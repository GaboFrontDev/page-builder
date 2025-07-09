from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from ...domain.entities import PlanType, SubscriptionStatus


class CreateSubscriptionDTO(BaseModel):
    user_id: int
    email: EmailStr
    plan_type: PlanType
    payment_method_id: Optional[str] = None


class SubscriptionResponseDTO(BaseModel):
    id: str
    user_id: int
    plan_type: PlanType
    status: SubscriptionStatus
    current_period_end: datetime
    is_active: bool


class CancelSubscriptionDTO(BaseModel):
    user_id: int


class CheckPremiumFeaturesDTO(BaseModel):
    user_id: int


class CheckPremiumFeaturesResponseDTO(BaseModel):
    has_premium_features: bool
    plan_type: Optional[PlanType] = None
    subscription_status: Optional[SubscriptionStatus] = None


class CreateCustomerDTO(BaseModel):
    user_id: int
    email: EmailStr
    name: Optional[str] = None


class CustomerResponseDTO(BaseModel):
    id: str
    user_id: int
    email: str
    stripe_customer_id: str
    name: Optional[str] = None


class SetupPaymentMethodDTO(BaseModel):
    user_id: int
    

class SetupPaymentMethodResponseDTO(BaseModel):
    client_secret: str
    customer_id: str