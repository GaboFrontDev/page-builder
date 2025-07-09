from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import (
    StripeCustomer, 
    StripeSubscription, 
    StripePaymentMethod, 
    StripeTransaction,
    StripePrice
)


class StripeCustomerRepository(ABC):
    """Repositorio para gestionar customers de Stripe en base de datos local"""
    
    @abstractmethod
    async def create_customer(self, customer: StripeCustomer) -> StripeCustomer:
        pass
    
    @abstractmethod
    async def get_customer_by_stripe_id(self, stripe_customer_id: str) -> Optional[StripeCustomer]:
        pass
    
    @abstractmethod
    async def get_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        pass
    
    @abstractmethod
    async def update_customer(self, customer: StripeCustomer) -> StripeCustomer:
        pass
    
    @abstractmethod
    async def delete_customer(self, stripe_customer_id: str) -> bool:
        pass


class StripeSubscriptionRepository(ABC):
    """Repositorio para gestionar suscripciones de Stripe en base de datos local"""
    
    @abstractmethod
    async def create_subscription(self, subscription: StripeSubscription) -> StripeSubscription:
        pass
    
    @abstractmethod
    async def get_subscription_by_stripe_id(self, stripe_subscription_id: str) -> Optional[StripeSubscription]:
        pass
    
    @abstractmethod
    async def get_subscriptions_by_customer_id(self, stripe_customer_id: str) -> List[StripeSubscription]:
        pass
    
    @abstractmethod
    async def update_subscription(self, subscription: StripeSubscription) -> StripeSubscription:
        pass
    
    @abstractmethod
    async def delete_subscription(self, stripe_subscription_id: str) -> bool:
        pass


class StripePaymentMethodRepository(ABC):
    """Repositorio para gestionar métodos de pago de Stripe en base de datos local"""
    
    @abstractmethod
    async def create_payment_method(self, payment_method: StripePaymentMethod) -> StripePaymentMethod:
        pass
    
    @abstractmethod
    async def get_payment_methods_by_customer_id(self, stripe_customer_id: str) -> List[StripePaymentMethod]:
        pass
    
    @abstractmethod
    async def get_payment_method_by_stripe_id(self, stripe_payment_method_id: str) -> Optional[StripePaymentMethod]:
        pass
    
    @abstractmethod
    async def get_default_payment_method(self, stripe_customer_id: str) -> Optional[StripePaymentMethod]:
        pass
    
    @abstractmethod
    async def update_payment_method(self, payment_method: StripePaymentMethod) -> StripePaymentMethod:
        pass
    
    @abstractmethod
    async def delete_payment_method(self, stripe_payment_method_id: str) -> bool:
        pass


class StripeTransactionRepository(ABC):
    """Repositorio para gestionar transacciones/eventos de Stripe en base de datos local"""
    
    @abstractmethod
    async def create_transaction(self, transaction: StripeTransaction) -> StripeTransaction:
        pass
    
    @abstractmethod
    async def get_transaction_by_stripe_event_id(self, stripe_event_id: str) -> Optional[StripeTransaction]:
        pass
    
    @abstractmethod
    async def get_transactions_by_object_id(self, object_id: str) -> List[StripeTransaction]:
        pass
    
    @abstractmethod
    async def update_transaction(self, transaction: StripeTransaction) -> StripeTransaction:
        pass


class StripePriceRepository(ABC):
    """Repositorio para gestionar precios de Stripe en base de datos local"""
    
    @abstractmethod
    async def create_price(self, price: StripePrice) -> StripePrice:
        pass
    
    @abstractmethod
    async def get_price_by_stripe_id(self, stripe_price_id: str) -> Optional[StripePrice]:
        pass
    
    @abstractmethod
    async def get_active_prices(self) -> List[StripePrice]:
        pass
    
    @abstractmethod
    async def update_price(self, price: StripePrice) -> StripePrice:
        pass