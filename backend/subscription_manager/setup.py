from sqlalchemy.orm import Session
from stripe_module.domain.events import InMemoryEventPublisher
from stripe_module.domain.entities import StripeEventType
from .stripe_event_handler import create_stripe_subscription_handler
import logging

logger = logging.getLogger(__name__)

# Instancia global del event publisher
event_publisher = InMemoryEventPublisher()

def setup_subscription_manager(db: Session) -> None:
    """Configura el sistema de gestión de suscripciones"""
    try:
        # Crear el handler de eventos
        handler = create_stripe_subscription_handler(db)
        
        # Suscribir el handler a los eventos de Stripe que nos interesan
        event_publisher.subscribe(StripeEventType.CUSTOMER_CREATED, handler)
        event_publisher.subscribe(StripeEventType.SUBSCRIPTION_CREATED, handler)
        event_publisher.subscribe(StripeEventType.INVOICE_PAYMENT_SUCCEEDED, handler)
        event_publisher.subscribe(StripeEventType.INVOICE_PAYMENT_FAILED, handler)
        event_publisher.subscribe(StripeEventType.SUBSCRIPTION_DELETED, handler)
        
        logger.info("Sistema de gestión de suscripciones configurado exitosamente")
        
    except Exception as e:
        logger.error(f"Error configurando sistema de gestión de suscripciones: {str(e)}")
        raise

def get_event_publisher() -> InMemoryEventPublisher:
    """Retorna la instancia global del event publisher"""
    return event_publisher