from abc import ABC, abstractmethod
from typing import List, Callable, Dict, Any
from .stripe_events import StripeEvent, StripeEventType


class EventPublisher(ABC):
    """Interfaz para publicar eventos"""
    
    @abstractmethod
    async def publish(self, event: StripeEvent) -> None:
        """Publicar un evento"""
        pass


class EventSubscriber(ABC):
    """Interfaz para suscribirse a eventos"""
    
    @abstractmethod
    async def handle(self, event: StripeEvent) -> None:
        """Manejar un evento"""
        pass


class InMemoryEventPublisher(EventPublisher):
    """Implementación en memoria del event publisher"""
    
    def __init__(self):
        self.subscribers: Dict[StripeEventType, List[EventSubscriber]] = {}
    
    def subscribe(self, event_type: StripeEventType, subscriber: EventSubscriber):
        """Suscribir un subscriber a un tipo de evento"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)
    
    async def publish(self, event: StripeEvent) -> None:
        """Publicar un evento a todos los subscribers"""
        if event.event_type in self.subscribers:
            for subscriber in self.subscribers[event.event_type]:
                try:
                    await subscriber.handle(event)
                except Exception as e:
                    # Log error pero no detener el procesamiento
                    print(f"Error handling event {event.event_type}: {str(e)}")


class StripeEventPublisher:
    """Publisher específico para eventos de Stripe"""
    
    def __init__(self, publisher: EventPublisher):
        self.publisher = publisher
    
    async def publish_customer_created(self, customer_id: str, email: str, metadata: Dict[str, Any] = None):
        """Publicar evento de customer creado"""
        from .stripe_events import StripeEventData
        from datetime import datetime
        
        event_data = StripeEventData(
            stripe_event_id="",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id=customer_id,
            customer_id=customer_id,
            metadata=metadata or {},
            occurred_at=datetime.utcnow()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=datetime.utcnow()
        )
        
        await self.publisher.publish(event)
    
    async def publish_subscription_created(
        self, 
        subscription_id: str, 
        customer_id: str, 
        price_id: str,
        metadata: Dict[str, Any] = None
    ):
        """Publicar evento de suscripción creada"""
        from .stripe_events import StripeEventData
        from datetime import datetime
        
        event_data = StripeEventData(
            stripe_event_id="",
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            metadata=metadata or {},
            occurred_at=datetime.utcnow()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_CREATED,
            data=event_data,
            created_at=datetime.utcnow()
        )
        
        await self.publisher.publish(event)
    
    async def publish_subscription_canceled(
        self, 
        subscription_id: str, 
        customer_id: str,
        metadata: Dict[str, Any] = None
    ):
        """Publicar evento de suscripción cancelada"""
        from .stripe_events import StripeEventData
        from datetime import datetime
        
        event_data = StripeEventData(
            stripe_event_id="",
            event_type=StripeEventType.SUBSCRIPTION_CANCELED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            metadata=metadata or {},
            occurred_at=datetime.utcnow()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.SUBSCRIPTION_CANCELED,
            data=event_data,
            created_at=datetime.utcnow()
        )
        
        await self.publisher.publish(event)
    
    async def publish_payment_succeeded(
        self, 
        customer_id: str, 
        subscription_id: str,
        amount: int,
        currency: str,
        metadata: Dict[str, Any] = None
    ):
        """Publicar evento de pago exitoso"""
        from .stripe_events import StripeEventData
        from datetime import datetime
        
        event_data = StripeEventData(
            stripe_event_id="",
            event_type=StripeEventType.PAYMENT_SUCCEEDED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            amount=amount,
            currency=currency,
            metadata=metadata or {},
            occurred_at=datetime.utcnow()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.PAYMENT_SUCCEEDED,
            data=event_data,
            created_at=datetime.utcnow()
        )
        
        await self.publisher.publish(event)
    
    async def publish_payment_failed(
        self, 
        customer_id: str, 
        subscription_id: str,
        amount: int,
        currency: str,
        error_message: str,
        metadata: Dict[str, Any] = None
    ):
        """Publicar evento de pago fallido"""
        from .stripe_events import StripeEventData
        from datetime import datetime
        
        event_data = StripeEventData(
            stripe_event_id="",
            event_type=StripeEventType.PAYMENT_FAILED,
            object_id=subscription_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            amount=amount,
            currency=currency,
            status="failed",
            metadata=metadata or {},
            occurred_at=datetime.utcnow()
        )
        
        event = StripeEvent(
            event_type=StripeEventType.PAYMENT_FAILED,
            data=event_data,
            created_at=datetime.utcnow()
        )
        
        await self.publisher.publish(event)