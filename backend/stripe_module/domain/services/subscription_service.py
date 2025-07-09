from typing import Optional, Dict, Any
from datetime import datetime

from ..entities import Subscription, Customer, PaymentMethod, PlanType, SubscriptionStatus
from ..repositories import SubscriptionRepository, CustomerRepository, StripeService


class SubscriptionDomainService:
    def __init__(
        self, 
        subscription_repo: SubscriptionRepository,
        customer_repo: CustomerRepository,
        stripe_service: StripeService
    ):
        self.subscription_repo = subscription_repo
        self.customer_repo = customer_repo
        self.stripe_service = stripe_service
    
    async def activate_user_subscription(
        self, 
        user_id: int, 
        email: str, 
        plan_type: PlanType,
        payment_method_id: Optional[str] = None
    ) -> Subscription:
        
        # Verificar si el usuario ya tiene una suscripción activa
        existing_subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if existing_subscription and existing_subscription.status == SubscriptionStatus.ACTIVE:
            raise ValueError("User already has an active subscription")
        
        # Crear o obtener customer en Stripe
        customer = await self._get_or_create_customer(user_id, email)
        
        # Obtener price_id basado en el plan
        price_id = self._get_price_id_for_plan(plan_type)
        
        # Crear suscripción en Stripe
        stripe_subscription = await self.stripe_service.create_subscription(
            customer.stripe_customer_id, 
            price_id, 
            payment_method_id
        )
        
        # Crear suscripción en la base de datos
        subscription = Subscription(
            stripe_subscription_id=stripe_subscription["id"],
            user_id=user_id,
            plan_type=plan_type,
            status=SubscriptionStatus(stripe_subscription["status"]),
            current_period_start=datetime.fromtimestamp(stripe_subscription["current_period_start"]),
            current_period_end=datetime.fromtimestamp(stripe_subscription["current_period_end"])
        )
        
        return await self.subscription_repo.create_subscription(subscription)
    
    async def cancel_user_subscription(self, user_id: int) -> bool:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if not subscription:
            raise ValueError("User has no active subscription")
        
        # Cancelar en Stripe
        await self.stripe_service.cancel_subscription(subscription.stripe_subscription_id)
        
        # Actualizar estado en la base de datos
        subscription.status = SubscriptionStatus.CANCELED
        await self.subscription_repo.update_subscription(subscription)
        
        return True
    
    async def check_user_has_premium_features(self, user_id: int) -> bool:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if not subscription:
            return False
        
        return (
            subscription.status == SubscriptionStatus.ACTIVE and 
            subscription.plan_type in [PlanType.BASIC, PlanType.PREMIUM, PlanType.ENTERPRISE]
        )
    
    async def get_user_subscription_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if not subscription:
            return None
        
        return {
            "plan_type": subscription.plan_type,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end,
            "is_active": subscription.status == SubscriptionStatus.ACTIVE
        }
    
    async def _get_or_create_customer(self, user_id: int, email: str) -> Customer:
        customer = await self.customer_repo.get_customer_by_user_id(user_id)
        if customer:
            return customer
        
        # Crear customer en Stripe
        stripe_customer = await self.stripe_service.create_customer(email)
        
        # Crear customer en la base de datos
        customer = Customer(
            stripe_customer_id=stripe_customer["id"],
            user_id=user_id,
            email=email
        )
        
        return await self.customer_repo.create_customer(customer)
    
    def _get_price_id_for_plan(self, plan_type: PlanType) -> str:
        price_mapping = {
            PlanType.BASIC: "price_basic_monthly",  # Reemplazar con price_id real
            PlanType.PREMIUM: "price_premium_monthly",  # Reemplazar con price_id real
            PlanType.ENTERPRISE: "price_enterprise_monthly"  # Reemplazar con price_id real
        }
        
        price_id = price_mapping.get(plan_type)
        if not price_id:
            raise ValueError(f"No price configured for plan type: {plan_type}")
        
        return price_id