from typing import List, Optional
from datetime import datetime

from ..dto import (
    CreateStripeCustomerDTO,
    StripeCustomerResponseDTO,
    CreateStripeSubscriptionDTO,
    StripeSubscriptionResponseDTO,
    CancelStripeSubscriptionDTO,
    SetupStripePaymentMethodDTO,
    SetupStripePaymentMethodResponseDTO,
    StripePaymentMethodResponseDTO,
    SyncStripeObjectDTO,
    StripeWebhookEventDTO,
    StripeTransactionResponseDTO,
    StripePriceResponseDTO,
    GetStripeCustomerSubscriptionsDTO,
    GetStripeCustomerPaymentMethodsDTO,
    ProcessStripeWebhookDTO
)
from ...domain.services import StripeDomainService
from ...domain.events import StripeEventPublisher


class CreateStripeCustomerUseCase:
    """Caso de uso para crear un customer en Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService, event_publisher: StripeEventPublisher):
        self.stripe_service = stripe_service
        self.event_publisher = event_publisher
    
    async def execute(self, request: CreateStripeCustomerDTO) -> StripeCustomerResponseDTO:
        customer = await self.stripe_service.create_customer_with_sync(
            email=request.email,
            name=request.name
        )
        
        # Publicar evento
        await self.event_publisher.publish_customer_created(
            customer_id=customer.stripe_customer_id,
            email=customer.email,
            metadata=request.metadata or {}
        )
        
        return StripeCustomerResponseDTO(
            id=customer.id,
            stripe_customer_id=customer.stripe_customer_id,
            email=customer.email,
            name=customer.name,
            phone=customer.phone,
            metadata=customer.metadata,
            created_at=customer.created_at
        )


class CreateStripeSubscriptionUseCase:
    """Caso de uso para crear una suscripción en Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService, event_publisher: StripeEventPublisher):
        self.stripe_service = stripe_service
        self.event_publisher = event_publisher
    
    async def execute(self, request: CreateStripeSubscriptionDTO) -> StripeSubscriptionResponseDTO:
        subscription = await self.stripe_service.create_subscription_with_sync(
            customer_id=request.customer_id,
            price_id=request.price_id,
            payment_method_id=request.payment_method_id,
            trial_period_days=request.trial_period_days
        )
        
        # Publicar evento
        await self.event_publisher.publish_subscription_created(
            subscription_id=subscription.stripe_subscription_id,
            customer_id=subscription.stripe_customer_id,
            price_id=subscription.stripe_price_id,
            metadata=request.metadata or {}
        )
        
        return StripeSubscriptionResponseDTO(
            id=subscription.id,
            stripe_subscription_id=subscription.stripe_subscription_id,
            stripe_customer_id=subscription.stripe_customer_id,
            stripe_price_id=subscription.stripe_price_id,
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            canceled_at=subscription.canceled_at,
            trial_start=subscription.trial_start,
            trial_end=subscription.trial_end,
            metadata=subscription.metadata,
            created_at=subscription.created_at
        )


class CancelStripeSubscriptionUseCase:
    """Caso de uso para cancelar una suscripción en Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService, event_publisher: StripeEventPublisher):
        self.stripe_service = stripe_service
        self.event_publisher = event_publisher
    
    async def execute(self, request: CancelStripeSubscriptionDTO) -> StripeSubscriptionResponseDTO:
        subscription = await self.stripe_service.cancel_subscription_with_sync(
            subscription_id=request.subscription_id
        )
        
        # Publicar evento
        await self.event_publisher.publish_subscription_canceled(
            subscription_id=subscription.stripe_subscription_id,
            customer_id=subscription.stripe_customer_id
        )
        
        return StripeSubscriptionResponseDTO(
            id=subscription.id,
            stripe_subscription_id=subscription.stripe_subscription_id,
            stripe_customer_id=subscription.stripe_customer_id,
            stripe_price_id=subscription.stripe_price_id,
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            canceled_at=subscription.canceled_at,
            trial_start=subscription.trial_start,
            trial_end=subscription.trial_end,
            metadata=subscription.metadata,
            created_at=subscription.created_at
        )


class SetupStripePaymentMethodUseCase:
    """Caso de uso para configurar un método de pago en Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self, request: SetupStripePaymentMethodDTO) -> SetupStripePaymentMethodResponseDTO:
        setup_intent = await self.stripe_service.stripe_service.create_setup_intent(
            customer_id=request.customer_id
        )
        
        return SetupStripePaymentMethodResponseDTO(
            client_secret=setup_intent["client_secret"],
            customer_id=request.customer_id,
            setup_intent_id=setup_intent["id"]
        )


class GetStripeCustomerSubscriptionsUseCase:
    """Caso de uso para obtener suscripciones de un customer"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self, request: GetStripeCustomerSubscriptionsDTO) -> List[StripeSubscriptionResponseDTO]:
        subscriptions = await self.stripe_service.get_customer_subscriptions(request.customer_id)
        
        return [
            StripeSubscriptionResponseDTO(
                id=sub.id,
                stripe_subscription_id=sub.stripe_subscription_id,
                stripe_customer_id=sub.stripe_customer_id,
                stripe_price_id=sub.stripe_price_id,
                status=sub.status,
                current_period_start=sub.current_period_start,
                current_period_end=sub.current_period_end,
                cancel_at_period_end=sub.cancel_at_period_end,
                canceled_at=sub.canceled_at,
                trial_start=sub.trial_start,
                trial_end=sub.trial_end,
                metadata=sub.metadata,
                created_at=sub.created_at
            )
            for sub in subscriptions
        ]


class GetStripeCustomerPaymentMethodsUseCase:
    """Caso de uso para obtener métodos de pago de un customer"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self, request: GetStripeCustomerPaymentMethodsDTO) -> List[StripePaymentMethodResponseDTO]:
        payment_methods = await self.stripe_service.payment_method_repo.get_payment_methods_by_customer_id(
            request.customer_id
        )
        
        return [
            StripePaymentMethodResponseDTO(
                id=pm.id,
                stripe_payment_method_id=pm.stripe_payment_method_id,
                stripe_customer_id=pm.stripe_customer_id,
                type=pm.type,
                card_last4=pm.card_last4,
                card_brand=pm.card_brand,
                card_exp_month=pm.card_exp_month,
                card_exp_year=pm.card_exp_year,
                is_default=pm.is_default,
                created_at=pm.created_at
            )
            for pm in payment_methods
        ]


class SyncStripeObjectUseCase:
    """Caso de uso para sincronizar objetos desde Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self, request: SyncStripeObjectDTO) -> Optional[dict]:
        if request.object_type == "customer":
            customer = await self.stripe_service.sync_customer_from_stripe(request.object_id)
            return {
                "type": "customer",
                "data": StripeCustomerResponseDTO(
                    id=customer.id,
                    stripe_customer_id=customer.stripe_customer_id,
                    email=customer.email,
                    name=customer.name,
                    phone=customer.phone,
                    metadata=customer.metadata,
                    created_at=customer.created_at
                ).dict()
            }
        elif request.object_type == "subscription":
            subscription = await self.stripe_service.sync_subscription_from_stripe(request.object_id)
            return {
                "type": "subscription",
                "data": StripeSubscriptionResponseDTO(
                    id=subscription.id,
                    stripe_subscription_id=subscription.stripe_subscription_id,
                    stripe_customer_id=subscription.stripe_customer_id,
                    stripe_price_id=subscription.stripe_price_id,
                    status=subscription.status,
                    current_period_start=subscription.current_period_start,
                    current_period_end=subscription.current_period_end,
                    cancel_at_period_end=subscription.cancel_at_period_end,
                    canceled_at=subscription.canceled_at,
                    trial_start=subscription.trial_start,
                    trial_end=subscription.trial_end,
                    metadata=subscription.metadata,
                    created_at=subscription.created_at
                ).dict()
            }
        
        return None


class ProcessStripeWebhookUseCase:
    """Caso de uso para procesar webhooks de Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self, request: ProcessStripeWebhookDTO) -> StripeTransactionResponseDTO:
        # Verificar firma del webhook
        event_data = self.stripe_service.stripe_service.verify_webhook_signature(
            payload=request.payload.encode(),
            signature=request.signature
        )
        
        # Procesar evento
        transaction = await self.stripe_service.process_stripe_event(event_data)
        
        return StripeTransactionResponseDTO(
            id=transaction.id,
            stripe_event_id=transaction.stripe_event_id,
            event_type=transaction.event_type,
            object_id=transaction.object_id,
            amount=transaction.amount,
            currency=transaction.currency,
            status=transaction.status,
            metadata=transaction.metadata,
            processed_at=transaction.processed_at,
            created_at=transaction.created_at
        )


class GetStripePricesUseCase:
    """Caso de uso para obtener precios de Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self) -> List[StripePriceResponseDTO]:
        prices = await self.stripe_service.get_active_prices()
        
        return [
            StripePriceResponseDTO(
                id=price.id,
                stripe_price_id=price.stripe_price_id,
                stripe_product_id=price.stripe_product_id,
                amount=price.amount,
                currency=price.currency,
                interval=price.interval,
                interval_count=price.interval_count,
                active=price.active,
                nickname=price.nickname,
                metadata=price.metadata,
                created_at=price.created_at
            )
            for price in prices
        ]


class SyncStripePricesUseCase:
    """Caso de uso para sincronizar precios desde Stripe"""
    
    def __init__(self, stripe_service: StripeDomainService):
        self.stripe_service = stripe_service
    
    async def execute(self) -> List[StripePriceResponseDTO]:
        prices = await self.stripe_service.sync_prices_from_stripe()
        
        return [
            StripePriceResponseDTO(
                id=price.id,
                stripe_price_id=price.stripe_price_id,
                stripe_product_id=price.stripe_product_id,
                amount=price.amount,
                currency=price.currency,
                interval=price.interval,
                interval_count=price.interval_count,
                active=price.active,
                nickname=price.nickname,
                metadata=price.metadata,
                created_at=price.created_at
            )
            for price in prices
        ]