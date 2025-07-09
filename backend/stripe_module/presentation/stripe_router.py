from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from typing import Optional
import json

from ..application import (
    CreateSubscriptionUseCase,
    CancelSubscriptionUseCase,
    CheckPremiumFeaturesUseCase,
    CreateCustomerUseCase,
    SetupPaymentMethodUseCase,
    GetUserSubscriptionUseCase,
    CreateSubscriptionDTO,
    CancelSubscriptionDTO,
    CheckPremiumFeaturesDTO,
    CreateCustomerDTO,
    SetupPaymentMethodDTO
)
from ..infrastructure import StripeClient
from ..domain.entities import PlanType

router = APIRouter(prefix="/stripe", tags=["stripe"])


# Dependency injection (se implementará en el factory)
def get_stripe_client():
    return StripeClient()


def get_create_subscription_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


def get_cancel_subscription_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


def get_check_premium_features_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


def get_create_customer_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


def get_setup_payment_method_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


def get_user_subscription_use_case(stripe_client: StripeClient = Depends(get_stripe_client)):
    # Esta función se implementará completamente en el factory
    pass


# Endpoints
@router.post("/subscriptions/create")
async def create_subscription(
    subscription_data: CreateSubscriptionDTO,
    use_case: CreateSubscriptionUseCase = Depends(get_create_subscription_use_case)
):
    """Crear una nueva suscripción para un usuario"""
    try:
        result = await use_case.execute(subscription_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Subscription created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/subscriptions/cancel")
async def cancel_subscription(
    cancel_data: CancelSubscriptionDTO,
    use_case: CancelSubscriptionUseCase = Depends(get_cancel_subscription_use_case)
):
    """Cancelar la suscripción de un usuario"""
    try:
        result = await use_case.execute(cancel_data)
        return {
            "success": result,
            "message": "Subscription canceled successfully" if result else "Failed to cancel subscription"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/{user_id}/premium-features")
async def check_premium_features(
    user_id: int,
    use_case: CheckPremiumFeaturesUseCase = Depends(get_check_premium_features_use_case)
):
    """Verificar si un usuario tiene acceso a features premium"""
    try:
        request_data = CheckPremiumFeaturesDTO(user_id=user_id)
        result = await use_case.execute(request_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Premium features status retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/{user_id}/subscription")
async def get_user_subscription(
    user_id: int,
    use_case: GetUserSubscriptionUseCase = Depends(get_user_subscription_use_case)
):
    """Obtener información de la suscripción de un usuario"""
    try:
        result = await use_case.execute(user_id)
        return {
            "success": True,
            "data": result.dict() if result else None,
            "message": "User subscription retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/customers/create")
async def create_customer(
    customer_data: CreateCustomerDTO,
    use_case: CreateCustomerUseCase = Depends(get_create_customer_use_case)
):
    """Crear un customer en Stripe"""
    try:
        result = await use_case.execute(customer_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Customer created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/payment-methods/setup")
async def setup_payment_method(
    setup_data: SetupPaymentMethodDTO,
    use_case: SetupPaymentMethodUseCase = Depends(get_setup_payment_method_use_case)
):
    """Configurar un método de pago para un usuario"""
    try:
        result = await use_case.execute(setup_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Payment method setup initiated successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/plans")
async def get_available_plans():
    """Obtener planes disponibles"""
    try:
        plans = [
            {
                "id": "basic",
                "name": "Basic",
                "description": "Plan básico con funcionalidades limitadas",
                "price": 9.99,
                "currency": "USD",
                "interval": "month",
                "features": [
                    "Hasta 10 páginas",
                    "Hasta 20 componentes por página",
                    "Soporte básico"
                ]
            },
            {
                "id": "premium",
                "name": "Premium",
                "description": "Plan premium con todas las funcionalidades",
                "price": 29.99,
                "currency": "USD",
                "interval": "month",
                "features": [
                    "Páginas ilimitadas",
                    "Componentes ilimitados",
                    "Dominio personalizado",
                    "Exportación de código",
                    "Templates premium",
                    "Soporte prioritario"
                ]
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "description": "Plan empresarial con funcionalidades avanzadas",
                "price": 99.99,
                "currency": "USD",
                "interval": "month",
                "features": [
                    "Todo lo del plan Premium",
                    "API access",
                    "Colaboración en equipo",
                    "Soporte 24/7",
                    "Integración personalizada"
                ]
            }
        ]
        
        return {
            "success": True,
            "data": plans,
            "message": "Plans retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/webhooks/stripe")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    stripe_client: StripeClient = Depends(get_stripe_client)
):
    """Manejar webhooks de Stripe"""
    try:
        body = await request.body()
        
        # Verificar la firma del webhook
        event = stripe_client.verify_webhook_signature(body, stripe_signature)
        
        # Procesar el evento
        if event["type"] == "customer.subscription.created":
            # Manejar nueva suscripción
            subscription = event["data"]["object"]
            # Actualizar base de datos
            pass
        elif event["type"] == "customer.subscription.updated":
            # Manejar actualización de suscripción
            subscription = event["data"]["object"]
            # Actualizar base de datos
            pass
        elif event["type"] == "customer.subscription.deleted":
            # Manejar cancelación de suscripción
            subscription = event["data"]["object"]
            # Actualizar base de datos
            pass
        elif event["type"] == "invoice.payment_succeeded":
            # Manejar pago exitoso
            invoice = event["data"]["object"]
            # Actualizar base de datos
            pass
        elif event["type"] == "invoice.payment_failed":
            # Manejar pago fallido
            invoice = event["data"]["object"]
            # Actualizar base de datos
            pass
        
        return JSONResponse(
            status_code=200,
            content={"received": True}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/{user_id}/usage-limits")
async def get_user_usage_limits(
    user_id: int,
    use_case: CheckPremiumFeaturesUseCase = Depends(get_check_premium_features_use_case)
):
    """Obtener límites de uso para un usuario"""
    try:
        request_data = CheckPremiumFeaturesDTO(user_id=user_id)
        result = await use_case.execute(request_data)
        
        # Definir límites basados en el plan
        limits = {
            "max_pages": 3,
            "max_components_per_page": 10,
            "can_use_custom_domain": False,
            "can_export_code": False,
            "can_use_premium_templates": False
        }
        
        if result.has_premium_features:
            if result.plan_type == PlanType.BASIC:
                limits = {
                    "max_pages": 10,
                    "max_components_per_page": 20,
                    "can_use_custom_domain": False,
                    "can_export_code": False,
                    "can_use_premium_templates": False
                }
            elif result.plan_type in [PlanType.PREMIUM, PlanType.ENTERPRISE]:
                limits = {
                    "max_pages": -1,  # Ilimitado
                    "max_components_per_page": -1,  # Ilimitado
                    "can_use_custom_domain": True,
                    "can_export_code": True,
                    "can_use_premium_templates": True
                }
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "plan_type": result.plan_type,
                "limits": limits
            },
            "message": "Usage limits retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")