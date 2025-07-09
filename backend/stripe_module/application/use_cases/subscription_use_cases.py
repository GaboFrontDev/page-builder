from typing import Optional

from ..dto import (
    CreateSubscriptionDTO,
    SubscriptionResponseDTO,
    CancelSubscriptionDTO,
    CheckPremiumFeaturesDTO,
    CheckPremiumFeaturesResponseDTO,
    CreateCustomerDTO,
    CustomerResponseDTO,
    SetupPaymentMethodDTO,
    SetupPaymentMethodResponseDTO
)
from ...domain.services import SubscriptionDomainService
from ...domain.repositories import CustomerRepository, StripeService
from ...domain.entities import SubscriptionStatus


class CreateSubscriptionUseCase:
    def __init__(self, subscription_service: SubscriptionDomainService):
        self.subscription_service = subscription_service
    
    async def execute(self, request: CreateSubscriptionDTO) -> SubscriptionResponseDTO:
        subscription = await self.subscription_service.activate_user_subscription(
            user_id=request.user_id,
            email=request.email,
            plan_type=request.plan_type,
            payment_method_id=request.payment_method_id
        )
        
        return SubscriptionResponseDTO(
            id=subscription.stripe_subscription_id,
            user_id=subscription.user_id,
            plan_type=subscription.plan_type,
            status=subscription.status,
            current_period_end=subscription.current_period_end,
            is_active=subscription.status == SubscriptionStatus.ACTIVE
        )


class CancelSubscriptionUseCase:
    def __init__(self, subscription_service: SubscriptionDomainService):
        self.subscription_service = subscription_service
    
    async def execute(self, request: CancelSubscriptionDTO) -> bool:
        return await self.subscription_service.cancel_user_subscription(request.user_id)


class CheckPremiumFeaturesUseCase:
    def __init__(self, subscription_service: SubscriptionDomainService):
        self.subscription_service = subscription_service
    
    async def execute(self, request: CheckPremiumFeaturesDTO) -> CheckPremiumFeaturesResponseDTO:
        has_premium = await self.subscription_service.check_user_has_premium_features(request.user_id)
        subscription_info = await self.subscription_service.get_user_subscription_info(request.user_id)
        
        return CheckPremiumFeaturesResponseDTO(
            has_premium_features=has_premium,
            plan_type=subscription_info.get("plan_type") if subscription_info else None,
            subscription_status=subscription_info.get("status") if subscription_info else None
        )


class CreateCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository, stripe_service: StripeService):
        self.customer_repo = customer_repo
        self.stripe_service = stripe_service
    
    async def execute(self, request: CreateCustomerDTO) -> CustomerResponseDTO:
        # Verificar si el customer ya existe
        existing_customer = await self.customer_repo.get_customer_by_user_id(request.user_id)
        if existing_customer:
            return CustomerResponseDTO(
                id=existing_customer.id,
                user_id=existing_customer.user_id,
                email=existing_customer.email,
                stripe_customer_id=existing_customer.stripe_customer_id,
                name=existing_customer.name
            )
        
        # Crear customer en Stripe
        stripe_customer = await self.stripe_service.create_customer(
            email=request.email,
            name=request.name
        )
        
        # Crear customer en la base de datos
        from ...domain.entities import Customer
        customer = Customer(
            stripe_customer_id=stripe_customer["id"],
            user_id=request.user_id,
            email=request.email,
            name=request.name
        )
        
        created_customer = await self.customer_repo.create_customer(customer)
        
        return CustomerResponseDTO(
            id=created_customer.id,
            user_id=created_customer.user_id,
            email=created_customer.email,
            stripe_customer_id=created_customer.stripe_customer_id,
            name=created_customer.name
        )


class SetupPaymentMethodUseCase:
    def __init__(self, customer_repo: CustomerRepository, stripe_service: StripeService):
        self.customer_repo = customer_repo
        self.stripe_service = stripe_service
    
    async def execute(self, request: SetupPaymentMethodDTO) -> SetupPaymentMethodResponseDTO:
        # Obtener customer
        customer = await self.customer_repo.get_customer_by_user_id(request.user_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Crear setup intent en Stripe
        setup_intent = await self.stripe_service.create_setup_intent(customer.stripe_customer_id)
        
        return SetupPaymentMethodResponseDTO(
            client_secret=setup_intent["client_secret"],
            customer_id=customer.stripe_customer_id
        )


class GetUserSubscriptionUseCase:
    def __init__(self, subscription_service: SubscriptionDomainService):
        self.subscription_service = subscription_service
    
    async def execute(self, user_id: int) -> Optional[SubscriptionResponseDTO]:
        subscription_info = await self.subscription_service.get_user_subscription_info(user_id)
        if not subscription_info:
            return None
        
        return SubscriptionResponseDTO(
            id="",  # Se puede obtener de la base de datos si es necesario
            user_id=user_id,
            plan_type=subscription_info["plan_type"],
            status=subscription_info["status"],
            current_period_end=subscription_info["current_period_end"],
            is_active=subscription_info["is_active"]
        )