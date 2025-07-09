import os
from typing import Dict, Optional
from pydantic import BaseModel


class StripeConfig(BaseModel):
    """Configuración para Stripe"""
    
    # Claves de API
    print(os.getenv("STRIPE_SECRET_KEY"))
    print(os.getenv("STRIPE_PUBLISHABLE_KEY"))
    print(os.getenv("STRIPE_WEBHOOK_SECRET"))
    print(os.getenv("STRIPE_PRICE_BASIC"))
    print(os.getenv("STRIPE_PRICE_PREMIUM"))
    print(os.getenv("STRIPE_PRICE_ENTERPRISE"))
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "sk_test_default")
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_default")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test_default")
    
    # Configuración de precios
    price_basic_monthly: str = os.getenv("STRIPE_PRICE_BASIC", "price_basic_default")
    price_premium_monthly: str = os.getenv("STRIPE_PRICE_PREMIUM", "price_premium_default")
    price_enterprise_monthly: str = os.getenv("STRIPE_PRICE_ENTERPRISE", "price_enterprise_default")
    
    # Configuración opcional
    stripe_api_version: str = "2023-10-16"
    
    # URLs de redirección
    success_url: str = "http://localhost:3000/success"
    cancel_url: str = "http://localhost:3000/cancel"
    
    # Configuración de desarrollo
    is_development: bool = True
    
    @property
    def price_mapping(self) -> Dict[str, str]:
        """Mapeo de tipos de plan a price_id de Stripe"""
        return {
            "basic": self.price_basic_monthly,
            "premium": self.price_premium_monthly,
            "enterprise": self.price_enterprise_monthly
        }
    
    def get_price_id(self, plan_type: str) -> Optional[str]:
        """Obtiene el price_id para un tipo de plan específico"""
        return self.price_mapping.get(plan_type.lower())
    
    def validate_configuration(self) -> bool:
        """Valida que la configuración esté completa"""
        required_fields = [
            self.stripe_secret_key,
            self.stripe_publishable_key,
            self.stripe_webhook_secret,
            self.price_basic_monthly,
            self.price_premium_monthly,
            self.price_enterprise_monthly
        ]
        
        return all(field for field in required_fields)