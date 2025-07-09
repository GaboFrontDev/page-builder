from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from typing import List
import json

from ..application import (
    CreateStripeCustomerUseCase,
    CreateStripeSubscriptionUseCase,
    CancelStripeSubscriptionUseCase,
    SetupStripePaymentMethodUseCase,
    GetStripeCustomerSubscriptionsUseCase,
    GetStripeCustomerPaymentMethodsUseCase,
    SyncStripeObjectUseCase,
    ProcessStripeWebhookUseCase,
    GetStripePricesUseCase,
    SyncStripePricesUseCase,
    CreateStripeCustomerDTO,
    CreateStripeSubscriptionDTO,
    CancelStripeSubscriptionDTO,
    SetupStripePaymentMethodDTO,
    GetStripeCustomerSubscriptionsDTO,
    GetStripeCustomerPaymentMethodsDTO,
    SyncStripeObjectDTO,
    ProcessStripeWebhookDTO
)

router = APIRouter(prefix="/stripe", tags=["stripe"])


# Dependency injection placeholders (se implementarán en el factory)
def get_create_customer_use_case():
    pass

def get_create_subscription_use_case():
    pass

def get_cancel_subscription_use_case():
    pass

def get_setup_payment_method_use_case():
    pass

def get_customer_subscriptions_use_case():
    pass

def get_customer_payment_methods_use_case():
    pass

def get_sync_object_use_case():
    pass

def get_process_webhook_use_case():
    pass

def get_prices_use_case():
    pass

def get_sync_prices_use_case():
    pass


@router.post("/customers", summary="Crear Customer en Stripe")
async def create_stripe_customer(
    customer_data: CreateStripeCustomerDTO,
    use_case: CreateStripeCustomerUseCase = Depends(get_create_customer_use_case)
):
    """
    Crear un customer en Stripe y sincronizar con base de datos local.
    Este endpoint solo maneja la creación del customer en Stripe.
    """
    try:
        result = await use_case.execute(customer_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Stripe customer created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/subscriptions", summary="Crear Suscripción en Stripe")
async def create_stripe_subscription(
    subscription_data: CreateStripeSubscriptionDTO,
    use_case: CreateStripeSubscriptionUseCase = Depends(get_create_subscription_use_case)
):
    """
    Crear una suscripción en Stripe y sincronizar con base de datos local.
    Este endpoint solo maneja la creación de la suscripción en Stripe.
    """
    try:
        result = await use_case.execute(subscription_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Stripe subscription created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/subscriptions/{subscription_id}", summary="Cancelar Suscripción en Stripe")
async def cancel_stripe_subscription(
    subscription_id: str,
    immediately: bool = False,
    use_case: CancelStripeSubscriptionUseCase = Depends(get_cancel_subscription_use_case)
):
    """
    Cancelar una suscripción en Stripe y sincronizar con base de datos local.
    Este endpoint solo maneja la cancelación en Stripe.
    """
    try:
        cancel_data = CancelStripeSubscriptionDTO(
            subscription_id=subscription_id,
            immediately=immediately
        )
        result = await use_case.execute(cancel_data)
        return {
            "success": True,
            "data": result.dict(),
            "message": "Stripe subscription canceled successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/payment-methods/setup", summary="Configurar Método de Pago en Stripe")
async def setup_stripe_payment_method(
    setup_data: SetupStripePaymentMethodDTO,
    use_case: SetupStripePaymentMethodUseCase = Depends(get_setup_payment_method_use_case)
):
    """
    Configurar un método de pago en Stripe.
    Retorna el client_secret para completar la configuración en el frontend.
    """
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


@router.get("/customers/{customer_id}/subscriptions", summary="Obtener Suscripciones del Customer")
async def get_customer_subscriptions(
    customer_id: str,
    use_case: GetStripeCustomerSubscriptionsUseCase = Depends(get_customer_subscriptions_use_case)
):
    """
    Obtener todas las suscripciones de un customer de Stripe.
    """
    try:
        request_data = GetStripeCustomerSubscriptionsDTO(customer_id=customer_id)
        result = await use_case.execute(request_data)
        return {
            "success": True,
            "data": [sub.dict() for sub in result],
            "message": "Customer subscriptions retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/customers/{customer_id}/payment-methods", summary="Obtener Métodos de Pago del Customer")
async def get_customer_payment_methods(
    customer_id: str,
    use_case: GetStripeCustomerPaymentMethodsUseCase = Depends(get_customer_payment_methods_use_case)
):
    """
    Obtener todos los métodos de pago de un customer de Stripe.
    """
    try:
        request_data = GetStripeCustomerPaymentMethodsDTO(customer_id=customer_id)
        result = await use_case.execute(request_data)
        return {
            "success": True,
            "data": [pm.dict() for pm in result],
            "message": "Customer payment methods retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/sync/{object_type}/{object_id}", summary="Sincronizar Objeto desde Stripe")
async def sync_stripe_object(
    object_type: str,
    object_id: str,
    use_case: SyncStripeObjectUseCase = Depends(get_sync_object_use_case)
):
    """
    Sincronizar un objeto específico desde Stripe hacia la base de datos local.
    object_type: 'customer' | 'subscription' | 'payment_method'
    """
    try:
        sync_data = SyncStripeObjectDTO(
            object_id=object_id,
            object_type=object_type
        )
        result = await use_case.execute(sync_data)
        return {
            "success": True,
            "data": result,
            "message": f"Stripe {object_type} synchronized successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/prices", summary="Obtener Precios de Stripe")
async def get_stripe_prices(
    use_case: GetStripePricesUseCase = Depends(get_prices_use_case)
):
    """
    Obtener todos los precios activos de Stripe desde la base de datos local.
    """
    try:
        result = await use_case.execute()
        return {
            "success": True,
            "data": [price.dict() for price in result],
            "message": "Stripe prices retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/prices/sync", summary="Sincronizar Precios desde Stripe")
async def sync_stripe_prices(
    use_case: SyncStripePricesUseCase = Depends(get_sync_prices_use_case)
):
    """
    Sincronizar todos los precios desde Stripe hacia la base de datos local.
    """
    try:
        result = await use_case.execute()
        return {
            "success": True,
            "data": [price.dict() for price in result],
            "message": "Stripe prices synchronized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/webhooks", summary="Webhook de Stripe")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    use_case: ProcessStripeWebhookUseCase = Depends(get_process_webhook_use_case)
):
    """
    Procesar webhooks de Stripe.
    Este endpoint recibe eventos de Stripe y los procesa/almacena localmente.
    Publica eventos para que otros módulos puedan reaccionar.
    """
    try:
        body = await request.body()
        
        webhook_data = ProcessStripeWebhookDTO(
            payload=body.decode(),
            signature=stripe_signature
        )
        
        result = await use_case.execute(webhook_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result.dict(),
                "message": "Webhook processed successfully"
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health", summary="Health Check del Módulo Stripe")
async def stripe_health_check():
    """
    Verificar el estado del módulo de Stripe.
    """
    try:
        # Verificar configuración básica
        from ..infrastructure.config import stripe_config
        
        config_valid = stripe_config.validate_configuration()
        
        return {
            "success": True,
            "data": {
                "module": "stripe",
                "status": "healthy" if config_valid else "unhealthy",
                "config_valid": config_valid,
                "stripe_api_version": stripe_config.stripe_api_version
            },
            "message": "Stripe module health check completed"
        }
    except Exception as e:
        return {
            "success": False,
            "data": {
                "module": "stripe",
                "status": "unhealthy",
                "error": str(e)
            },
            "message": "Stripe module health check failed"
        }


@router.get("/events/{event_id}", summary="Obtener Evento de Stripe")
async def get_stripe_event(
    event_id: str,
    # use_case: GetStripeEventUseCase = Depends(get_stripe_event_use_case)
):
    """
    Obtener información de un evento específico de Stripe.
    """
    # TODO: Implementar caso de uso para obtener eventos
    return {
        "success": False,
        "message": "Not implemented yet"
    }


@router.get("/transactions", summary="Obtener Transacciones de Stripe")
async def get_stripe_transactions(
    limit: int = 10,
    offset: int = 0,
    # use_case: GetStripeTransactionsUseCase = Depends(get_stripe_transactions_use_case)
):
    """
    Obtener historial de transacciones de Stripe.
    """
    # TODO: Implementar caso de uso para obtener transacciones
    return {
        "success": False,
        "message": "Not implemented yet"
    }