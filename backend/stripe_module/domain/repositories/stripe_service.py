from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class StripeService(ABC):
    
    @abstractmethod
    async def create_customer(self, email: str, name: Optional[str] = None) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update_customer(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_subscription(
        self, 
        customer_id: str, 
        price_id: str, 
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update_subscription(self, subscription_id: str, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_payment_method(
        self, 
        customer_id: str, 
        payment_method_type: str = "card"
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def attach_payment_method(self, payment_method_id: str, customer_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def detach_payment_method(self, payment_method_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_payment_methods(self, customer_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_setup_intent(self, customer_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def confirm_setup_intent(self, setup_intent_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_prices(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_price(self, price_id: str) -> Dict[str, Any]:
        pass