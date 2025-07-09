from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

from ...domain.entities import StripeSubscriptionStatus


class CreateStripeCustomerDTO(BaseModel):
    """DTO para crear un customer en Stripe"""
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class StripeCustomerResponseDTO(BaseModel):
    """DTO de respuesta para customer de Stripe"""
    id: str
    stripe_customer_id: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class CreateStripeSubscriptionDTO(BaseModel):
    """DTO para crear una suscripción en Stripe"""
    customer_id: str  # Stripe Customer ID
    price_id: str     # Stripe Price ID
    payment_method_id: Optional[str] = None
    trial_period_days: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class StripeSubscriptionResponseDTO(BaseModel):
    """DTO de respuesta para suscripción de Stripe"""
    id: str
    stripe_subscription_id: str
    stripe_customer_id: str
    stripe_price_id: str
    status: StripeSubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    canceled_at: Optional[datetime] = None
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class CancelStripeSubscriptionDTO(BaseModel):
    """DTO para cancelar una suscripción en Stripe"""
    subscription_id: str  # Stripe Subscription ID
    immediately: bool = False  # Si se cancela inmediatamente o al final del periodo


class SetupStripePaymentMethodDTO(BaseModel):
    """DTO para configurar un método de pago en Stripe"""
    customer_id: str  # Stripe Customer ID
    usage: str = "off_session"  # "on_session" | "off_session"
    payment_method_types: list = ["card"]


class SetupStripePaymentMethodResponseDTO(BaseModel):
    """DTO de respuesta para setup de método de pago"""
    client_secret: str
    customer_id: str
    setup_intent_id: str


class StripePaymentMethodResponseDTO(BaseModel):
    """DTO de respuesta para método de pago de Stripe"""
    id: str
    stripe_payment_method_id: str
    stripe_customer_id: str
    type: str
    card_last4: Optional[str] = None
    card_brand: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None
    is_default: bool = False
    created_at: Optional[datetime] = None


class SyncStripeObjectDTO(BaseModel):
    """DTO para sincronizar objetos desde Stripe"""
    object_id: str  # ID del objeto en Stripe
    object_type: str  # "customer" | "subscription" | "payment_method"


class StripeWebhookEventDTO(BaseModel):
    """DTO para eventos de webhook de Stripe"""
    stripe_event_id: str
    event_type: str
    object_data: Dict[str, Any]
    created_at: datetime


class StripeTransactionResponseDTO(BaseModel):
    """DTO de respuesta para transacción de Stripe"""
    id: str
    stripe_event_id: str
    event_type: str
    object_id: str
    amount: Optional[int] = None
    currency: Optional[str] = None
    status: str
    metadata: Optional[Dict[str, Any]] = None
    processed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class StripePriceResponseDTO(BaseModel):
    """DTO de respuesta para precio de Stripe"""
    id: str
    stripe_price_id: str
    stripe_product_id: str
    amount: int
    currency: str
    interval: str
    interval_count: int
    active: bool
    nickname: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class GetStripeCustomerSubscriptionsDTO(BaseModel):
    """DTO para obtener suscripciones de un customer"""
    customer_id: str  # Stripe Customer ID


class GetStripeCustomerPaymentMethodsDTO(BaseModel):
    """DTO para obtener métodos de pago de un customer"""
    customer_id: str  # Stripe Customer ID


class ProcessStripeWebhookDTO(BaseModel):
    """DTO para procesar webhook de Stripe"""
    payload: str
    signature: str