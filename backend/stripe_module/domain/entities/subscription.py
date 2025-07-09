from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel


class StripeSubscriptionStatus(str, Enum):
    ACTIVE = "active"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"


class StripeEventType(str, Enum):
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    INVOICE_PAYMENT_SUCCEEDED = "invoice.payment_succeeded"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    PAYMENT_METHOD_ATTACHED = "payment_method.attached"


class StripeCustomer(BaseModel):
    """Entidad que representa un customer de Stripe"""
    id: Optional[str] = None
    stripe_customer_id: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


class StripeSubscription(BaseModel):
    """Entidad que representa una suscripción de Stripe"""
    id: Optional[str] = None
    stripe_subscription_id: str
    stripe_customer_id: str
    stripe_price_id: str
    status: StripeSubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False
    canceled_at: Optional[datetime] = None
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


class StripePaymentMethod(BaseModel):
    """Entidad que representa un método de pago de Stripe"""
    id: Optional[str] = None
    stripe_payment_method_id: str
    stripe_customer_id: str
    type: str
    card_last4: Optional[str] = None
    card_brand: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None
    is_default: bool = False
    created_at: Optional[datetime] = None


class StripeTransaction(BaseModel):
    """Entidad que representa una transacción/evento de Stripe"""
    id: Optional[str] = None
    stripe_event_id: str
    event_type: StripeEventType
    object_id: str  # ID del objeto relacionado (customer, subscription, etc.)
    amount: Optional[int] = None  # En centavos
    currency: Optional[str] = None
    status: str
    metadata: Optional[Dict[str, Any]] = None
    processed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


class StripePrice(BaseModel):
    """Entidad que representa un precio de Stripe"""
    id: Optional[str] = None
    stripe_price_id: str
    stripe_product_id: str
    amount: int  # En centavos
    currency: str
    interval: str  # month, year, etc.
    interval_count: int = 1
    active: bool = True
    nickname: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None