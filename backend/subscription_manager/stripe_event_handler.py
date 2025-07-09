from sqlalchemy.orm import Session
from stripe_module.domain.events import StripeEvent, EventSubscriber
from stripe_module.domain.entities import StripeEventType
from models import User
from database import get_db
import logging

logger = logging.getLogger(__name__)


class StripeSubscriptionEventHandler(EventSubscriber):
    """Handler para eventos de suscripción de Stripe"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def handle(self, event: StripeEvent) -> None:
        """Maneja eventos de Stripe y actualiza el estado de suscripción del usuario"""
        try:
            if event.event_type == StripeEventType.CUSTOMER_CREATED:
                await self._handle_customer_created(event)
            elif event.event_type == StripeEventType.SUBSCRIPTION_CREATED:
                await self._handle_subscription_created(event)
            elif event.event_type == StripeEventType.INVOICE_PAYMENT_SUCCEEDED:
                await self._handle_payment_succeeded(event)
            elif event.event_type == StripeEventType.INVOICE_PAYMENT_FAILED:
                await self._handle_payment_failed(event)
            elif event.event_type == StripeEventType.SUBSCRIPTION_DELETED:
                await self._handle_subscription_canceled(event)
            else:
                logger.info(f"Evento no manejado: {event.event_type}")
                
        except Exception as e:
            logger.error(f"Error manejando evento {event.event_type}: {str(e)}")
            raise
    
    async def _handle_customer_created(self, event: StripeEvent) -> None:
        """Maneja la creación de un customer en Stripe"""
        customer_id = event.data.customer_id
        email = event.data.metadata.get('email') if event.data.metadata else None
        
        if not email:
            logger.warning(f"No se encontró email en metadata del customer {customer_id}")
            return
        
        # Buscar al usuario por email y actualizar su stripe_customer_id
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            user.stripe_customer_id = customer_id
            self.db.commit()
            logger.info(f"Usuario {user.email} asociado con customer {customer_id}")
        else:
            logger.warning(f"No se encontró usuario con email {email}")
    
    async def _handle_subscription_created(self, event: StripeEvent) -> None:
        """Maneja la creación de una suscripción"""
        customer_id = event.data.customer_id
        
        if not customer_id:
            logger.warning("No se encontró customer_id en evento de suscripción")
            return
        
        # Encontrar al usuario por stripe_customer_id y activar suscripción
        user = self.db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_active = True
            self.db.commit()
            logger.info(f"Suscripción activada para usuario {user.email}")
        else:
            logger.warning(f"No se encontró usuario con stripe_customer_id {customer_id}")
    
    async def _handle_payment_succeeded(self, event: StripeEvent) -> None:
        """Maneja pagos exitosos"""
        customer_id = event.data.customer_id
        
        if not customer_id:
            logger.warning("No se encontró customer_id en evento de pago")
            return
        
        # Asegurar que la suscripción esté activa
        user = self.db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_active = True
            self.db.commit()
            logger.info(f"Suscripción confirmada activa para usuario {user.email} tras pago exitoso")
        else:
            logger.warning(f"No se encontró usuario con stripe_customer_id {customer_id}")
    
    async def _handle_payment_failed(self, event: StripeEvent) -> None:
        """Maneja pagos fallidos"""
        customer_id = event.data.customer_id
        
        if not customer_id:
            logger.warning("No se encontró customer_id en evento de pago fallido")
            return
        
        # Por ahora solo logeamos, podrías agregar lógica para suspender tras varios fallos
        user = self.db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            logger.warning(f"Pago fallido para usuario {user.email}")
            # Aquí podrías agregar lógica para manejar pagos fallidos
            # Por ejemplo, enviar email o suspender tras X intentos fallidos
        else:
            logger.warning(f"No se encontró usuario con stripe_customer_id {customer_id}")
    
    async def _handle_subscription_canceled(self, event: StripeEvent) -> None:
        """Maneja la cancelación de una suscripción"""
        customer_id = event.data.customer_id
        
        if not customer_id:
            logger.warning("No se encontró customer_id en evento de cancelación")
            return
        
        # Desactivar la suscripción del usuario
        user = self.db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_active = False
            self.db.commit()
            logger.info(f"Suscripción desactivada para usuario {user.email}")
        else:
            logger.warning(f"No se encontró usuario con stripe_customer_id {customer_id}")


def create_stripe_subscription_handler(db: Session) -> StripeSubscriptionEventHandler:
    """Factory para crear el handler de eventos de suscripción"""
    return StripeSubscriptionEventHandler(db)