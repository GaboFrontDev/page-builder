import stripe
from typing import Dict, Any, Optional
import asyncio

from ...domain.repositories import StripeService
from ..config import StripeConfig


class StripeClient(StripeService):
    def __init__(self, config: Optional[StripeConfig] = None):
        if config:
            self.config = config
        else:
            self.config = StripeConfig()
        
        # Configurar Stripe
        stripe.api_key = self.config.stripe_secret_key
        stripe.api_version = self.config.stripe_api_version
    
    async def create_customer(self, email: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Crear un customer en Stripe"""
        try:
            customer_data = {"email": email}
            if name:
                customer_data["name"] = name
            
            loop = asyncio.get_event_loop()
            customer = await loop.run_in_executor(
                None, 
                lambda: stripe.Customer.create(**customer_data)
            )
            return customer
        except Exception as e:
            raise ValueError(f"Error creating customer: {str(e)}")
    
    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Obtener un customer de Stripe"""
        try:
            loop = asyncio.get_event_loop()
            customer = await loop.run_in_executor(
                None, 
                lambda: stripe.Customer.retrieve(customer_id)
            )
            return customer
        except Exception as e:
            raise ValueError(f"Error retrieving customer: {str(e)}")
    
    async def update_customer(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        """Actualizar un customer en Stripe"""
        try:
            loop = asyncio.get_event_loop()
            customer = await loop.run_in_executor(
                None, 
                lambda: stripe.Customer.modify(customer_id, **kwargs)
            )
            return customer
        except Exception as e:
            raise ValueError(f"Error updating customer: {str(e)}")
    
    async def create_subscription(
        self, 
        customer_id: str, 
        price_id: str, 
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear una suscripción en Stripe"""
        try:
            subscription_data = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "payment_behavior": "default_incomplete",
                "payment_settings": {
                    "save_default_payment_method": "on_subscription"
                },
                "expand": ["latest_invoice.payment_intent"]
            }
            
            if payment_method_id:
                subscription_data["default_payment_method"] = payment_method_id
            
            loop = asyncio.get_event_loop()
            subscription = await loop.run_in_executor(
                None, 
                lambda: stripe.Subscription.create(**subscription_data)
            )
            return subscription
        except Exception as e:
            raise ValueError(f"Error creating subscription: {str(e)}")
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Obtener una suscripción de Stripe"""
        try:
            loop = asyncio.get_event_loop()
            subscription = await loop.run_in_executor(
                None, 
                lambda: stripe.Subscription.retrieve(subscription_id)
            )
            return subscription
        except Exception as e:
            raise ValueError(f"Error retrieving subscription: {str(e)}")
    
    async def update_subscription(self, subscription_id: str, **kwargs) -> Dict[str, Any]:
        """Actualizar una suscripción en Stripe"""
        try:
            loop = asyncio.get_event_loop()
            subscription = await loop.run_in_executor(
                None, 
                lambda: stripe.Subscription.modify(subscription_id, **kwargs)
            )
            return subscription
        except Exception as e:
            raise ValueError(f"Error updating subscription: {str(e)}")
    
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancelar una suscripción en Stripe"""
        try:
            loop = asyncio.get_event_loop()
            subscription = await loop.run_in_executor(
                None, 
                lambda: stripe.Subscription.delete(subscription_id)
            )
            return subscription
        except Exception as e:
            raise ValueError(f"Error canceling subscription: {str(e)}")
    
    async def create_payment_method(
        self, 
        customer_id: str, 
        payment_method_type: str = "card"
    ) -> Dict[str, Any]:
        """Crear un método de pago en Stripe"""
        try:
            loop = asyncio.get_event_loop()
            payment_method = await loop.run_in_executor(
                None, 
                lambda: stripe.PaymentMethod.create(
                    type=payment_method_type,
                    customer=customer_id
                )
            )
            return payment_method
        except Exception as e:
            raise ValueError(f"Error creating payment method: {str(e)}")
    
    async def attach_payment_method(self, payment_method_id: str, customer_id: str) -> Dict[str, Any]:
        """Asociar un método de pago a un customer"""
        try:
            loop = asyncio.get_event_loop()
            payment_method = await loop.run_in_executor(
                None, 
                lambda: stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer_id
                )
            )
            return payment_method
        except Exception as e:
            raise ValueError(f"Error attaching payment method: {str(e)}")
    
    async def detach_payment_method(self, payment_method_id: str) -> Dict[str, Any]:
        """Desasociar un método de pago"""
        try:
            loop = asyncio.get_event_loop()
            payment_method = await loop.run_in_executor(
                None, 
                lambda: stripe.PaymentMethod.detach(payment_method_id)
            )
            return payment_method
        except Exception as e:
            raise ValueError(f"Error detaching payment method: {str(e)}")
    
    async def get_payment_methods(self, customer_id: str) -> Dict[str, Any]:
        """Obtener los métodos de pago de un customer"""
        try:
            loop = asyncio.get_event_loop()
            payment_methods = await loop.run_in_executor(
                None, 
                lambda: stripe.PaymentMethod.list(
                    customer=customer_id,
                    type="card"
                )
            )
            return payment_methods
        except Exception as e:
            raise ValueError(f"Error retrieving payment methods: {str(e)}")
    
    async def create_setup_intent(self, customer_id: str) -> Dict[str, Any]:
        """Crear un setup intent para configurar métodos de pago"""
        try:
            loop = asyncio.get_event_loop()
            setup_intent = await loop.run_in_executor(
                None, 
                lambda: stripe.SetupIntent.create(
                    customer=customer_id,
                    payment_method_types=["card"],
                    usage="off_session"
                )
            )
            return setup_intent
        except Exception as e:
            raise ValueError(f"Error creating setup intent: {str(e)}")
    
    async def confirm_setup_intent(self, setup_intent_id: str) -> Dict[str, Any]:
        """Confirmar un setup intent"""
        try:
            loop = asyncio.get_event_loop()
            setup_intent = await loop.run_in_executor(
                None, 
                lambda: stripe.SetupIntent.confirm(setup_intent_id)
            )
            return setup_intent
        except Exception as e:
            raise ValueError(f"Error confirming setup intent: {str(e)}")
    
    async def get_prices(self) -> Dict[str, Any]:
        """Obtener todos los precios disponibles"""
        try:
            loop = asyncio.get_event_loop()
            prices = await loop.run_in_executor(
                None, 
                lambda: stripe.Price.list(active=True)
            )
            return prices
        except Exception as e:
            raise ValueError(f"Error retrieving prices: {str(e)}")
    
    async def get_price(self, price_id: str) -> Dict[str, Any]:
        """Obtener un precio específico"""
        try:
            loop = asyncio.get_event_loop()
            price = await loop.run_in_executor(
                None, 
                lambda: stripe.Price.retrieve(price_id)
            )
            return price
        except Exception as e:
            raise ValueError(f"Error retrieving price: {str(e)}")
    
    async def create_webhook_endpoint(self, url: str, events: list) -> Dict[str, Any]:
        """Crear un webhook endpoint"""
        try:
            loop = asyncio.get_event_loop()
            webhook_endpoint = await loop.run_in_executor(
                None, 
                lambda: stripe.WebhookEndpoint.create(
                    url=url,
                    enabled_events=events
                )
            )
            return webhook_endpoint
        except Exception as e:
            raise ValueError(f"Error creating webhook endpoint: {str(e)}")
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Verificar la firma de un webhook"""
        try:
            event = stripe.Webhook.construct_event(
                payload, 
                signature, 
                self.config.stripe_webhook_secret
            )
            return event
        except ValueError as e:
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise ValueError("Invalid signature")