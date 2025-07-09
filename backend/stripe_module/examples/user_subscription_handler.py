"""
Ejemplo de cómo un módulo de usuario puede suscribirse a eventos de Stripe
para actualizar el estado de las features premium de los usuarios.

Este archivo es solo un ejemplo y debe ser implementado en el módulo de usuario.
"""

from typing import Dict, Any
from ..domain.events import EventSubscriber, StripeEvent, StripeEventType


class UserSubscriptionHandler(EventSubscriber):
    """
    Handler de ejemplo para actualizar el estado de usuario basado en eventos de Stripe.
    
    Este handler se ejecutaría en el módulo de usuario, no en el módulo de Stripe.
    """
    
    def __init__(self, user_service, user_repository):
        self.user_service = user_service
        self.user_repository = user_repository
    
    async def handle(self, event: StripeEvent) -> None:
        """Manejar eventos de Stripe y actualizar estado de usuario"""
        
        if event.event_type == StripeEventType.SUBSCRIPTION_CREATED:
            await self._handle_subscription_created(event)
        elif event.event_type == StripeEventType.SUBSCRIPTION_UPDATED:
            await self._handle_subscription_updated(event)
        elif event.event_type == StripeEventType.SUBSCRIPTION_CANCELED:
            await self._handle_subscription_canceled(event)
        elif event.event_type == StripeEventType.PAYMENT_SUCCEEDED:
            await self._handle_payment_succeeded(event)
        elif event.event_type == StripeEventType.PAYMENT_FAILED:
            await self._handle_payment_failed(event)
    
    async def _handle_subscription_created(self, event: StripeEvent):
        """Manejar nueva suscripción creada"""
        # Obtener información del evento
        customer_id = event.data.customer_id
        subscription_id = event.data.subscription_id
        
        # Buscar usuario por customer_id de Stripe
        user = await self._find_user_by_stripe_customer_id(customer_id)
        if not user:
            return
        
        # Actualizar estado del usuario
        await self.user_service.activate_premium_features(
            user_id=user.id,
            subscription_id=subscription_id,
            plan_type=self._get_plan_type_from_metadata(event.data.metadata)
        )
    
    async def _handle_subscription_updated(self, event: StripeEvent):
        """Manejar actualización de suscripción"""
        customer_id = event.data.customer_id
        subscription_id = event.data.subscription_id
        
        user = await self._find_user_by_stripe_customer_id(customer_id)
        if not user:
            return
        
        # Actualizar estado según el status de la suscripción
        subscription_status = event.data.status
        
        if subscription_status == "active":
            await self.user_service.activate_premium_features(
                user_id=user.id,
                subscription_id=subscription_id,
                plan_type=self._get_plan_type_from_metadata(event.data.metadata)
            )
        elif subscription_status in ["past_due", "unpaid"]:
            await self.user_service.suspend_premium_features(
                user_id=user.id,
                reason="payment_issue"
            )
    
    async def _handle_subscription_canceled(self, event: StripeEvent):
        """Manejar cancelación de suscripción"""
        customer_id = event.data.customer_id
        
        user = await self._find_user_by_stripe_customer_id(customer_id)
        if not user:
            return
        
        # Desactivar features premium
        await self.user_service.deactivate_premium_features(
            user_id=user.id,
            reason="subscription_canceled"
        )
    
    async def _handle_payment_succeeded(self, event: StripeEvent):
        """Manejar pago exitoso"""
        customer_id = event.data.customer_id
        subscription_id = event.data.subscription_id
        
        user = await self._find_user_by_stripe_customer_id(customer_id)
        if not user:
            return
        
        # Reactivar features si estaban suspendidas
        await self.user_service.reactivate_premium_features_if_suspended(
            user_id=user.id,
            subscription_id=subscription_id
        )
        
        # Registrar pago exitoso
        await self.user_service.record_successful_payment(
            user_id=user.id,
            amount=event.data.amount,
            currency=event.data.currency
        )
    
    async def _handle_payment_failed(self, event: StripeEvent):
        """Manejar pago fallido"""
        customer_id = event.data.customer_id
        subscription_id = event.data.subscription_id
        
        user = await self._find_user_by_stripe_customer_id(customer_id)
        if not user:
            return
        
        # Suspender features premium si es necesario
        await self.user_service.suspend_premium_features(
            user_id=user.id,
            reason="payment_failed"
        )
        
        # Registrar pago fallido
        await self.user_service.record_failed_payment(
            user_id=user.id,
            amount=event.data.amount,
            currency=event.data.currency
        )
    
    async def _find_user_by_stripe_customer_id(self, stripe_customer_id: str):
        """Buscar usuario por customer_id de Stripe"""
        # Esta función debe implementarse en el módulo de usuario
        # Ejemplo de implementación:
        # return await self.user_repository.find_by_stripe_customer_id(stripe_customer_id)
        pass
    
    def _get_plan_type_from_metadata(self, metadata: Dict[str, Any]) -> str:
        """Extraer tipo de plan desde metadata"""
        # Esta lógica depende de cómo se configure metadata en Stripe
        return metadata.get("plan_type", "basic")


# Ejemplo de cómo configurar el handler en el módulo de usuario
async def setup_stripe_event_handlers(event_publisher, user_service, user_repository):
    """
    Configurar handlers para eventos de Stripe.
    
    Esta función debe llamarse en el módulo de usuario durante la inicialización.
    """
    
    # Crear handler
    user_handler = UserSubscriptionHandler(user_service, user_repository)
    
    # Suscribir handler a eventos relevantes
    event_publisher.subscribe(StripeEventType.SUBSCRIPTION_CREATED, user_handler)
    event_publisher.subscribe(StripeEventType.SUBSCRIPTION_UPDATED, user_handler)
    event_publisher.subscribe(StripeEventType.SUBSCRIPTION_CANCELED, user_handler)
    event_publisher.subscribe(StripeEventType.PAYMENT_SUCCEEDED, user_handler)
    event_publisher.subscribe(StripeEventType.PAYMENT_FAILED, user_handler)


# Ejemplo de servicio de usuario que reacciona a eventos de Stripe
class UserService:
    """Ejemplo de servicio de usuario que maneja features premium"""
    
    def __init__(self, user_repository, user_feature_repository):
        self.user_repository = user_repository
        self.user_feature_repository = user_feature_repository
    
    async def activate_premium_features(self, user_id: int, subscription_id: str, plan_type: str):
        """Activar features premium para un usuario"""
        # Obtener configuración de features basada en el plan
        features = self._get_features_for_plan(plan_type)
        
        # Actualizar estado del usuario
        await self.user_feature_repository.update_user_features(
            user_id=user_id,
            features=features,
            subscription_id=subscription_id,
            is_active=True
        )
    
    async def deactivate_premium_features(self, user_id: int, reason: str):
        """Desactivar features premium para un usuario"""
        # Revertir a features gratuitas
        free_features = self._get_features_for_plan("free")
        
        await self.user_feature_repository.update_user_features(
            user_id=user_id,
            features=free_features,
            subscription_id=None,
            is_active=False,
            deactivation_reason=reason
        )
    
    async def suspend_premium_features(self, user_id: int, reason: str):
        """Suspender temporalmente features premium"""
        await self.user_feature_repository.suspend_user_features(
            user_id=user_id,
            suspension_reason=reason
        )
    
    async def reactivate_premium_features_if_suspended(self, user_id: int, subscription_id: str):
        """Reactivar features si estaban suspendidas"""
        user_features = await self.user_feature_repository.get_user_features(user_id)
        
        if user_features and user_features.is_suspended:
            await self.user_feature_repository.reactivate_user_features(
                user_id=user_id,
                subscription_id=subscription_id
            )
    
    async def record_successful_payment(self, user_id: int, amount: int, currency: str):
        """Registrar pago exitoso"""
        # Implementar lógica para registrar pago exitoso
        pass
    
    async def record_failed_payment(self, user_id: int, amount: int, currency: str):
        """Registrar pago fallido"""
        # Implementar lógica para registrar pago fallido
        pass
    
    def _get_features_for_plan(self, plan_type: str) -> Dict[str, Any]:
        """Obtener configuración de features para un plan"""
        features_config = {
            "free": {
                "max_pages": 3,
                "max_components_per_page": 10,
                "can_use_custom_domain": False,
                "can_export_code": False,
                "can_use_premium_templates": False,
                "can_use_analytics": False
            },
            "basic": {
                "max_pages": 10,
                "max_components_per_page": 25,
                "can_use_custom_domain": False,
                "can_export_code": True,
                "can_use_premium_templates": False,
                "can_use_analytics": True
            },
            "premium": {
                "max_pages": -1,  # Ilimitado
                "max_components_per_page": -1,  # Ilimitado
                "can_use_custom_domain": True,
                "can_export_code": True,
                "can_use_premium_templates": True,
                "can_use_analytics": True
            }
        }
        
        return features_config.get(plan_type, features_config["free"])