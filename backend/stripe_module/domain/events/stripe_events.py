from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class StripeEventStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class StripeEventType(str, Enum):
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"
    SUBSCRIPTION_CREATED = "subscription.created"
    SUBSCRIPTION_UPDATED = "subscription.updated"
    SUBSCRIPTION_CANCELED = "subscription.canceled"
    PAYMENT_SUCCEEDED = "payment.succeeded"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_METHOD_ATTACHED = "payment_method.attached"
    PAYMENT_METHOD_DETACHED = "payment_method.detached"


class StripeEventData(BaseModel):
    """Datos del evento de Stripe"""
    stripe_event_id: str
    event_type: StripeEventType
    object_id: str
    customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    amount: Optional[int] = None  # En centavos
    currency: Optional[str] = None
    status: Optional[str] = None
    metadata: Dict[str, Any] = {}
    occurred_at: datetime
    
    class Config:
        use_enum_values = True


class StripeEvent(BaseModel):
    """Evento de Stripe para comunicación entre módulos"""
    id: Optional[str] = None
    event_type: StripeEventType
    data: StripeEventData
    status: StripeEventStatus = StripeEventStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True
    
    def mark_as_processing(self):
        """Marcar evento como en procesamiento"""
        self.status = StripeEventStatus.PROCESSING
    
    def mark_as_completed(self):
        """Marcar evento como completado"""
        self.status = StripeEventStatus.COMPLETED
        self.processed_at = datetime.utcnow()
    
    def mark_as_failed(self, error_message: str):
        """Marcar evento como fallido"""
        self.status = StripeEventStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1
    
    def can_retry(self) -> bool:
        """Verificar si el evento puede ser reintentado"""
        return self.retry_count < self.max_retries and self.status == StripeEventStatus.FAILED