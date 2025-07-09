from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import get_current_active_user
from subscription_manager import StripeIntegrationService
from stripe_module.domain.services import StripeDomainService
from stripe_module.stripe_factory import get_stripe_factory
from typing import Dict, Any
import logging

router = APIRouter(prefix="/api/subscription", tags=["subscription"])
logger = logging.getLogger(__name__)

def get_stripe_integration_service(db: Session = Depends(get_db)) -> StripeIntegrationService:
    """Dependency para obtener el servicio de integración con Stripe"""
    stripe_factory = get_stripe_factory(db)
    stripe_domain_service = StripeDomainService(
        stripe_service=stripe_factory.get_stripe_client(),
        customer_repo=stripe_factory.get_customer_repository(),
        subscription_repo=stripe_factory.get_subscription_repository(),
        payment_method_repo=stripe_factory.get_payment_method_repository(),
        transaction_repo=stripe_factory.get_transaction_repository(),
        price_repo=stripe_factory.get_price_repository()
    )
    return StripeIntegrationService(stripe_domain_service, db)

@router.post("/test-customer-creation")
async def test_customer_creation(
    user_email: str,
    db: Session = Depends(get_db),
    stripe_integration: StripeIntegrationService = Depends(get_stripe_integration_service)
):
    """Endpoint de prueba para crear un customer y probar el sistema"""
    try:
        # Crear customer en Stripe con eventos
        customer = await stripe_integration.create_customer_with_events(
            email=user_email,
            name=f"Test User {user_email}"
        )
        
        # Verificar que el usuario se actualizó
        user = db.query(User).filter(User.email == user_email).first()
        user_info = {
            "exists": user is not None,
            "stripe_customer_id": user.stripe_customer_id if user else None,
            "subscription_active": user.subscription_active if user else None
        }
        
        return {
            "message": "Customer creado exitosamente",
            "stripe_customer": {
                "id": customer.id,
                "stripe_customer_id": customer.stripe_customer_id,
                "email": customer.email,
                "name": customer.name
            },
            "user_updated": user_info
        }
        
    except Exception as e:
        logger.error(f"Error creando customer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-subscription-creation")
async def test_subscription_creation(
    stripe_customer_id: str,
    price_id: str = "price_test_basic",
    db: Session = Depends(get_db),
    stripe_integration: StripeIntegrationService = Depends(get_stripe_integration_service)
):
    """Endpoint de prueba para crear una suscripción y probar el sistema"""
    try:
        # Crear suscripción en Stripe con eventos
        subscription = await stripe_integration.create_subscription_with_events(
            customer_id=stripe_customer_id,
            price_id=price_id
        )
        
        # Verificar que el usuario se actualizó
        user = db.query(User).filter(User.stripe_customer_id == stripe_customer_id).first()
        user_info = {
            "exists": user is not None,
            "email": user.email if user else None,
            "subscription_active": user.subscription_active if user else None
        }
        
        return {
            "message": "Suscripción creada exitosamente",
            "stripe_subscription": {
                "id": subscription.id,
                "stripe_subscription_id": subscription.stripe_subscription_id,
                "stripe_customer_id": subscription.stripe_customer_id,
                "status": subscription.status,
                "price_id": subscription.stripe_price_id
            },
            "user_updated": user_info
        }
        
    except Exception as e:
        logger.error(f"Error creando suscripción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-status/{user_id}")
async def get_user_subscription_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtener el estado de suscripción de un usuario"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "user_id": user.id,
            "email": user.email,
            "subscription_active": user.subscription_active,
            "stripe_customer_id": user.stripe_customer_id,
            "is_active": user.is_active
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de usuario: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-checkout-session")
async def create_checkout_session(
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    stripe_integration: StripeIntegrationService = Depends(get_stripe_integration_service)
):
    """Crear sesión de checkout de Stripe"""
    try:
        price_id = request.get("price_id")
        plan_type = request.get("plan_type")
        
        if not price_id or not plan_type:
            raise HTTPException(status_code=400, detail="price_id y plan_type son requeridos")
        
        # Crear o obtener customer
        customer = await stripe_integration.create_customer_with_events(
            email=current_user.email,
            name=current_user.username
        )
        
        # Crear checkout session
        session = await stripe_integration.create_checkout_session(
            customer_id=customer.stripe_customer_id,
            price_id=price_id,
            plan_type=plan_type,
            success_url="http://localhost:3000/dashboard?success=true",
            cancel_url="http://localhost:3000/subscription?canceled=true"
        )
        
        return {
            "session_url": session.url,
            "session_id": session.id
        }
        
    except Exception as e:
        logger.error(f"Error creando checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify-payment/{session_id}")
async def verify_payment(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Verificar si el pago fue exitoso y activar suscripción"""
    try:
        import stripe
        from stripe_module.infrastructure.config.stripe_config import StripeConfig
        
        config = StripeConfig()
        stripe.api_key = config.stripe_secret_key
        
        # Obtener la sesión de Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # Actualizar usuario
            current_user.subscription_active = True
            current_user.stripe_customer_id = session.customer
            db.commit()
            
            return {
                "success": True,
                "message": "Suscripción activada exitosamente"
            }
        else:
            return {
                "success": False,
                "message": "Pago no completado"
            }
            
    except Exception as e:
        logger.error(f"Error verificando pago: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def handle_stripe_webhook(
    webhook_data: Dict[str, Any],
    db: Session = Depends(get_db),
    stripe_integration: StripeIntegrationService = Depends(get_stripe_integration_service)
):
    """Webhook para procesar eventos de Stripe"""
    try:
        # Procesar webhook
        await stripe_integration.process_stripe_webhook(webhook_data)
        
        return {"status": "success", "message": "Webhook procesado exitosamente"}
        
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))