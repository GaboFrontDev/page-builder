import os
from typing import Optional

class StripeConfig:
    """Configuración para Stripe"""
    
    # Claves de API de Stripe
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_...")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
    
    # Webhook endpoint secret
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_...")
    
    # URLs de redirección
    SUCCESS_URL = os.getenv("SUCCESS_URL", "http://localhost:3000/dashboard?success=true")
    CANCEL_URL = os.getenv("CANCEL_URL", "http://localhost:3000/subscription?canceled=true")
    
    # Price IDs de los planes
    PRICE_IDS = {
        "basic": os.getenv("STRIPE_PRICE_BASIC", "price_basic_monthly"),
        "premium": os.getenv("STRIPE_PRICE_PREMIUM", "price_premium_monthly"),
        "enterprise": os.getenv("STRIPE_PRICE_ENTERPRISE", "price_enterprise_monthly")
    }
    
    @classmethod
    def get_price_id(cls, plan_type: str) -> Optional[str]:
        """Obtener el price ID para un tipo de plan"""
        return cls.PRICE_IDS.get(plan_type)
    
    @classmethod
    def is_test_mode(cls) -> bool:
        """Verificar si estamos en modo de prueba"""
        return cls.STRIPE_SECRET_KEY.startswith("sk_test_")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validar que la configuración esté completa"""
        required_keys = [
            cls.STRIPE_PUBLISHABLE_KEY,
            cls.STRIPE_SECRET_KEY
        ]
        
        return all(key and not key.endswith("...") for key in required_keys) 