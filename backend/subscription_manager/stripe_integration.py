from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from stripe_module.domain.entities import StripeCustomer, StripeSubscription, StripeEventType
from stripe_module.domain.events import StripeEvent, StripeEventData, StripeEventStatus
from stripe_module.domain.services import StripeDomainService
from .setup import get_event_publisher
import logging

logger = logging.getLogger(__name__)


class StripeIntegrationService:
    """Servicio que integra Stripe con el sistema de gestión de suscripciones"""
    
    def __init__(self, stripe_service: StripeDomainService, db: Session):
        self.stripe_service = stripe_service
        self.db = db
        self.event_publisher = get_event_publisher()
    
    async def create_customer_with_events(self, email: str, name: Optional[str] = None) -> StripeCustomer:
        """Crear customer en Stripe y publicar evento"""
        try:
            # Crear customer usando el servicio de Stripe
            customer = await self.stripe_service.create_customer_with_sync(email, name)
            
            # Publicar evento
            await self._publish_customer_created_event(customer)
            
            return customer
            
        except Exception as e:
            logger.error(f"Error creando customer: {str(e)}")
            raise
    
    async def create_subscription_with_events(
        self, 
        customer_id: str, 
        price_id: str,
        payment_method_id: Optional[str] = None,
        trial_period_days: Optional[int] = None
    ) -> StripeSubscription:
        """Crear suscripción en Stripe y publicar evento"""
        try:
            # Crear suscripción usando el servicio de Stripe
            subscription = await self.stripe_service.create_subscription_with_sync(
                customer_id, price_id, payment_method_id, trial_period_days
            )
            
            # Publicar evento
            await self._publish_subscription_created_event(subscription)
            
            return subscription
            
        except Exception as e:
            logger.error(f"Error creando suscripción: {str(e)}")
            raise

    async def create_checkout_session(
        self, 
        customer_id: str, 
        price_id: str, 
        plan_type: str,
        success_url: str,
        cancel_url: str
    ):
        """Crear sesión de checkout de Stripe"""
        try:
            import stripe
            from stripe_module.infrastructure.config.stripe_config import StripeConfig
            
            # Configurar Stripe
            config = StripeConfig()
            stripe.api_key = config.stripe_secret_key
            
            # Crear checkout session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{success_url}&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=cancel_url,
                metadata={
                    'plan_type': plan_type,
                    'customer_id': customer_id
                }
            )
            
            return session
            
        except Exception as e:
            logger.error(f"Error creando checkout session: {str(e)}")
            raise
    
    async def cancel_subscription_with_events(self, subscription_id: str) -> StripeSubscription:
        """Cancelar suscripción en Stripe y publicar evento"""
        try:
            # Cancelar suscripción usando el servicio de Stripe
            subscription = await self.stripe_service.cancel_subscription_with_sync(subscription_id)
            
            # Publicar evento
            await self._publish_subscription_canceled_event(subscription)
            
            return subscription
            
        except Exception as e:
            logger.error(f"Error cancelando suscripción: {str(e)}")
            raise
    
    async def process_stripe_webhook(self, event_data: Dict[str, Any]) -> None:
        """Procesar webhook de Stripe y publicar eventos correspondientes"""
        try:
            event_type = event_data.get("type")
            
            if event_type == "customer.created":
                await self._handle_customer_created_webhook(event_data)
            elif event_type == "customer.subscription.created":
                await self._handle_subscription_created_webhook(event_data)
            elif event_type == "customer.subscription.updated":
                await self._handle_subscription_updated_webhook(event_data)
            elif event_type == "invoice.payment_succeeded":
                await self._handle_payment_succeeded_webhook(event_data)
            elif event_type == "invoice.payment_failed":
                await self._handle_payment_failed_webhook(event_data)
            elif event_type == "customer.subscription.deleted":
                await self._handle_subscription_deleted_webhook(event_data)
            else:
                logger.info(f"Webhook no manejado: {event_type}")
                
        except Exception as e:
            logger.error(f"Error procesando webhook: {str(e)}")
            raise
    
    async def _publish_customer_created_event(self, customer: StripeCustomer) -> None:
        """Publicar evento de customer creado"""
        event_data = StripeEventData(
            stripe_event_id=f"evt_customer_created_{customer.stripe_customer_id}",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id=customer.stripe_customer_id,
            customer_id=customer.stripe_customer_id,
            metadata={"email": customer.email, **(customer.metadata or {})},
            occurred_at=datetime.now()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
        logger.info(f"Evento customer_created publicado para {customer.email}")
    
    async def _publish_subscription_created_event(self, subscription: StripeSubscription) -> None:
        """Publicar evento de suscripción creada"""
        event_data = StripeEventData(
            stripe_event_id=f"evt_subscription_created_{subscription.stripe_subscription_id}",
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            object_id=subscription.stripe_subscription_id,
            customer_id=subscription.stripe_customer_id,
            subscription_id=subscription.stripe_subscription_id,
            metadata=subscription.metadata or {},
            occurred_at=datetime.now()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            data=event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
        logger.info(f"Evento subscription_created publicado para customer {subscription.stripe_customer_id}")
    
    async def _publish_subscription_canceled_event(self, subscription: StripeSubscription) -> None:
        """Publicar evento de suscripción cancelada"""
        event_data = StripeEventData(
            stripe_event_id=f"evt_subscription_canceled_{subscription.stripe_subscription_id}",
            event_type=StripeEventType.SUBSCRIPTION_DELETED,
            object_id=subscription.stripe_subscription_id,
            customer_id=subscription.stripe_customer_id,
            subscription_id=subscription.stripe_subscription_id,
            metadata=subscription.metadata or {},
            occurred_at=datetime.now()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_DELETED,
            data=event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
        logger.info(f"Evento subscription_canceled publicado para customer {subscription.stripe_customer_id}")
    
    async def _handle_customer_created_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de customer creado"""
        customer_data = event_data.get("data", {}).get("object", {})
        customer_id = customer_data.get("id")
        
        if not customer_id:
            logger.warning("No se encontró customer_id en webhook")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id=customer_id,
            customer_id=customer_id,
            metadata=customer_data.get("metadata", {}),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
    
    async def _handle_subscription_created_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de suscripción creada"""
        subscription_data = event_data.get("data", {}).get("object", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer")
        
        if not subscription_id or not customer_id:
            logger.warning("No se encontró subscription_id o customer_id en webhook")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            metadata=subscription_data.get("metadata", {}),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
    
    async def _handle_subscription_updated_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de suscripción actualizada"""
        subscription_data = event_data.get("data", {}).get("object", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer")
        
        if not subscription_id or not customer_id:
            logger.warning("No se encontró subscription_id o customer_id en webhook de actualización")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.SUBSCRIPTION_UPDATED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            metadata=subscription_data.get("metadata", {}),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_UPDATED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
    
    async def _handle_payment_succeeded_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de pago exitoso"""
        invoice_data = event_data.get("data", {}).get("object", {})
        customer_id = invoice_data.get("customer")
        subscription_id = invoice_data.get("subscription")
        
        if not customer_id:
            logger.warning("No se encontró customer_id en webhook de pago")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.INVOICE_PAYMENT_SUCCEEDED,
            object_id=invoice_data.get("id"),
            customer_id=customer_id,
            subscription_id=subscription_id,
            amount=invoice_data.get("amount_paid"),
            currency=invoice_data.get("currency"),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.INVOICE_PAYMENT_SUCCEEDED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
    
    async def _handle_payment_failed_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de pago fallido"""
        invoice_data = event_data.get("data", {}).get("object", {})
        customer_id = invoice_data.get("customer")
        subscription_id = invoice_data.get("subscription")
        
        if not customer_id:
            logger.warning("No se encontró customer_id en webhook de pago fallido")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.INVOICE_PAYMENT_FAILED,
            object_id=invoice_data.get("id"),
            customer_id=customer_id,
            subscription_id=subscription_id,
            amount=invoice_data.get("amount_due"),
            currency=invoice_data.get("currency"),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.INVOICE_PAYMENT_FAILED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)
    
    async def _handle_subscription_deleted_webhook(self, event_data: Dict[str, Any]) -> None:
        """Manejar webhook de suscripción cancelada"""
        subscription_data = event_data.get("data", {}).get("object", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer")
        
        if not subscription_id or not customer_id:
            logger.warning("No se encontró subscription_id o customer_id en webhook de cancelación")
            return
        
        webhook_event_data = StripeEventData(
            stripe_event_id=event_data.get("id"),
            event_type=StripeEventType.SUBSCRIPTION_DELETED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            metadata=subscription_data.get("metadata", {}),
            occurred_at=datetime.fromtimestamp(event_data.get("created", 0))
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_DELETED,
            data=webhook_event_data,
            created_at=datetime.now()
        )
        
        await self.event_publisher.publish(event)