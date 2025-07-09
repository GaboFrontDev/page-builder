from typing import Optional, Dict, Any, List
from datetime import datetime

from ..entities import (
    StripeCustomer, 
    StripeSubscription, 
    StripePaymentMethod,
    StripeTransaction,
    StripePrice,
    StripeEventType,
    StripeSubscriptionStatus
)
from ..repositories import (
    StripeService,
    StripeCustomerRepository,
    StripeSubscriptionRepository,
    StripePaymentMethodRepository,
    StripeTransactionRepository,
    StripePriceRepository
)


class StripeDomainService:
    """Servicio de dominio para operaciones de Stripe"""
    
    def __init__(
        self,
        stripe_service: StripeService,
        customer_repo: StripeCustomerRepository,
        subscription_repo: StripeSubscriptionRepository,
        payment_method_repo: StripePaymentMethodRepository,
        transaction_repo: StripeTransactionRepository,
        price_repo: StripePriceRepository
    ):
        self.stripe_service = stripe_service
        self.customer_repo = customer_repo
        self.subscription_repo = subscription_repo
        self.payment_method_repo = payment_method_repo
        self.transaction_repo = transaction_repo
        self.price_repo = price_repo
    
    async def create_customer_with_sync(self, email: str, name: Optional[str] = None) -> StripeCustomer:
        """Crear customer en Stripe y sincronizar con BD local"""
        # Crear en Stripe
        stripe_customer_data = await self.stripe_service.create_customer(email, name)
        
        # Crear en BD local
        customer = StripeCustomer(
            stripe_customer_id=stripe_customer_data["id"],
            email=email,
            name=name,
            metadata=stripe_customer_data.get("metadata", {})
        )
        
        return await self.customer_repo.create_customer(customer)
    
    async def create_subscription_with_sync(
        self, 
        customer_id: str, 
        price_id: str,
        payment_method_id: Optional[str] = None,
        trial_period_days: Optional[int] = None
    ) -> StripeSubscription:
        """Crear suscripción en Stripe y sincronizar con BD local"""
        # Crear en Stripe
        stripe_subscription_data = await self.stripe_service.create_subscription(
            customer_id, 
            price_id, 
            payment_method_id
        )
        
        # Crear en BD local
        subscription = StripeSubscription(
            stripe_subscription_id=stripe_subscription_data["id"],
            stripe_customer_id=customer_id,
            stripe_price_id=price_id,
            status=StripeSubscriptionStatus(stripe_subscription_data["status"]),
            current_period_start=datetime.fromtimestamp(stripe_subscription_data["current_period_start"]),
            current_period_end=datetime.fromtimestamp(stripe_subscription_data["current_period_end"]),
            cancel_at_period_end=stripe_subscription_data.get("cancel_at_period_end", False),
            trial_start=datetime.fromtimestamp(stripe_subscription_data["trial_start"]) if stripe_subscription_data.get("trial_start") else None,
            trial_end=datetime.fromtimestamp(stripe_subscription_data["trial_end"]) if stripe_subscription_data.get("trial_end") else None,
            metadata=stripe_subscription_data.get("metadata", {})
        )
        
        return await self.subscription_repo.create_subscription(subscription)
    
    async def cancel_subscription_with_sync(self, subscription_id: str) -> StripeSubscription:
        """Cancelar suscripción en Stripe y sincronizar con BD local"""
        # Cancelar en Stripe
        stripe_subscription_data = await self.stripe_service.cancel_subscription(subscription_id)
        
        # Actualizar en BD local
        subscription = await self.subscription_repo.get_subscription_by_stripe_id(subscription_id)
        if subscription:
            subscription.status = StripeSubscriptionStatus(stripe_subscription_data["status"])
            subscription.canceled_at = datetime.fromtimestamp(stripe_subscription_data["canceled_at"]) if stripe_subscription_data.get("canceled_at") else None
            subscription.cancel_at_period_end = stripe_subscription_data.get("cancel_at_period_end", False)
            
            return await self.subscription_repo.update_subscription(subscription)
        
        raise ValueError("Subscription not found in local database")
    
    async def sync_customer_from_stripe(self, stripe_customer_id: str) -> StripeCustomer:
        """Sincronizar customer desde Stripe hacia BD local"""
        # Obtener desde Stripe
        stripe_customer_data = await self.stripe_service.get_customer(stripe_customer_id)
        
        # Verificar si existe en BD local
        existing_customer = await self.customer_repo.get_customer_by_stripe_id(stripe_customer_id)
        
        if existing_customer:
            # Actualizar existente
            existing_customer.email = stripe_customer_data["email"]
            existing_customer.name = stripe_customer_data.get("name")
            existing_customer.phone = stripe_customer_data.get("phone")
            existing_customer.metadata = stripe_customer_data.get("metadata", {})
            
            return await self.customer_repo.update_customer(existing_customer)
        else:
            # Crear nuevo
            customer = StripeCustomer(
                stripe_customer_id=stripe_customer_id,
                email=stripe_customer_data["email"],
                name=stripe_customer_data.get("name"),
                phone=stripe_customer_data.get("phone"),
                metadata=stripe_customer_data.get("metadata", {})
            )
            
            return await self.customer_repo.create_customer(customer)
    
    async def sync_subscription_from_stripe(self, stripe_subscription_id: str) -> StripeSubscription:
        """Sincronizar suscripción desde Stripe hacia BD local"""
        # Obtener desde Stripe
        stripe_subscription_data = await self.stripe_service.get_subscription(stripe_subscription_id)
        
        # Verificar si existe en BD local
        existing_subscription = await self.subscription_repo.get_subscription_by_stripe_id(stripe_subscription_id)
        
        if existing_subscription:
            # Actualizar existente
            existing_subscription.status = StripeSubscriptionStatus(stripe_subscription_data["status"])
            existing_subscription.current_period_start = datetime.fromtimestamp(stripe_subscription_data["current_period_start"])
            existing_subscription.current_period_end = datetime.fromtimestamp(stripe_subscription_data["current_period_end"])
            existing_subscription.cancel_at_period_end = stripe_subscription_data.get("cancel_at_period_end", False)
            existing_subscription.canceled_at = datetime.fromtimestamp(stripe_subscription_data["canceled_at"]) if stripe_subscription_data.get("canceled_at") else None
            existing_subscription.metadata = stripe_subscription_data.get("metadata", {})
            
            return await self.subscription_repo.update_subscription(existing_subscription)
        else:
            # Crear nuevo
            subscription = StripeSubscription(
                stripe_subscription_id=stripe_subscription_id,
                stripe_customer_id=stripe_subscription_data["customer"],
                stripe_price_id=stripe_subscription_data["items"]["data"][0]["price"]["id"],
                status=StripeSubscriptionStatus(stripe_subscription_data["status"]),
                current_period_start=datetime.fromtimestamp(stripe_subscription_data["current_period_start"]),
                current_period_end=datetime.fromtimestamp(stripe_subscription_data["current_period_end"]),
                cancel_at_period_end=stripe_subscription_data.get("cancel_at_period_end", False),
                canceled_at=datetime.fromtimestamp(stripe_subscription_data["canceled_at"]) if stripe_subscription_data.get("canceled_at") else None,
                trial_start=datetime.fromtimestamp(stripe_subscription_data["trial_start"]) if stripe_subscription_data.get("trial_start") else None,
                trial_end=datetime.fromtimestamp(stripe_subscription_data["trial_end"]) if stripe_subscription_data.get("trial_end") else None,
                metadata=stripe_subscription_data.get("metadata", {})
            )
            
            return await self.subscription_repo.create_subscription(subscription)
    
    async def process_stripe_event(self, event_data: Dict[str, Any]) -> StripeTransaction:
        """Procesar un evento de Stripe y registrar transacción"""
        # Verificar si el evento ya fue procesado
        existing_transaction = await self.transaction_repo.get_transaction_by_stripe_event_id(event_data["id"])
        if existing_transaction:
            return existing_transaction
        
        # Crear transacción
        transaction = StripeTransaction(
            stripe_event_id=event_data["id"],
            event_type=StripeEventType(event_data["type"]),
            object_id=event_data["data"]["object"]["id"],
            status="processed",
            metadata=event_data.get("data", {}).get("object", {}),
            processed_at=datetime.utcnow()
        )
        
        # Procesar según tipo de evento
        if event_data["type"] == "customer.created":
            await self.sync_customer_from_stripe(event_data["data"]["object"]["id"])
        elif event_data["type"] == "customer.subscription.created":
            await self.sync_subscription_from_stripe(event_data["data"]["object"]["id"])
        elif event_data["type"] == "customer.subscription.updated":
            await self.sync_subscription_from_stripe(event_data["data"]["object"]["id"])
        elif event_data["type"] == "customer.subscription.deleted":
            await self.sync_subscription_from_stripe(event_data["data"]["object"]["id"])
        elif event_data["type"] == "invoice.payment_succeeded":
            # Actualizar información de pago
            invoice_data = event_data["data"]["object"]
            transaction.amount = invoice_data.get("amount_paid", 0)
            transaction.currency = invoice_data.get("currency", "usd")
        elif event_data["type"] == "invoice.payment_failed":
            # Registrar pago fallido
            invoice_data = event_data["data"]["object"]
            transaction.amount = invoice_data.get("amount_due", 0)
            transaction.currency = invoice_data.get("currency", "usd")
            transaction.status = "failed"
        
        return await self.transaction_repo.create_transaction(transaction)
    
    async def get_customer_subscriptions(self, stripe_customer_id: str) -> List[StripeSubscription]:
        """Obtener todas las suscripciones de un customer"""
        return await self.subscription_repo.get_subscriptions_by_customer_id(stripe_customer_id)
    
    async def get_active_prices(self) -> List[StripePrice]:
        """Obtener precios activos"""
        return await self.price_repo.get_active_prices()
    
    async def sync_prices_from_stripe(self) -> List[StripePrice]:
        """Sincronizar precios desde Stripe"""
        stripe_prices_data = await self.stripe_service.get_prices()
        synced_prices = []
        
        for price_data in stripe_prices_data.get("data", []):
            existing_price = await self.price_repo.get_price_by_stripe_id(price_data["id"])
            
            if existing_price:
                # Actualizar existente
                existing_price.active = price_data.get("active", True)
                existing_price.nickname = price_data.get("nickname")
                existing_price.metadata = price_data.get("metadata", {})
                
                updated_price = await self.price_repo.update_price(existing_price)
                synced_prices.append(updated_price)
            else:
                # Crear nuevo
                price = StripePrice(
                    stripe_price_id=price_data["id"],
                    stripe_product_id=price_data["product"],
                    amount=price_data["unit_amount"],
                    currency=price_data["currency"],
                    interval=price_data.get("recurring", {}).get("interval", "month"),
                    interval_count=price_data.get("recurring", {}).get("interval_count", 1),
                    active=price_data.get("active", True),
                    nickname=price_data.get("nickname"),
                    metadata=price_data.get("metadata", {})
                )
                
                created_price = await self.price_repo.create_price(price)
                synced_prices.append(created_price)
        
        return synced_prices