import pytest
from unittest.mock import Mock
from datetime import datetime

from ..domain.entities import (
    StripeCustomer,
    StripeSubscription,
    StripePaymentMethod,
    StripeTransaction,
    StripePrice,
    StripeSubscriptionStatus,
    StripeEventType
)


@pytest.fixture
def sample_stripe_customer():
    """Customer de ejemplo para tests"""
    return StripeCustomer(
        id="1",
        stripe_customer_id="cus_test123",
        email="test@example.com",
        name="John Doe",
        phone="+1234567890",
        metadata={"user_id": "123"},
        created_at=datetime.now()
    )


@pytest.fixture
def sample_stripe_subscription():
    """Suscripción de ejemplo para tests"""
    return StripeSubscription(
        id="1",
        stripe_subscription_id="sub_test123",
        stripe_customer_id="cus_test123",
        stripe_price_id="price_test123",
        status=StripeSubscriptionStatus.ACTIVE,
        current_period_start=datetime.now(),
        current_period_end=datetime.now(),
        cancel_at_period_end=False,
        canceled_at=None,
        trial_start=None,
        trial_end=None,
        metadata={"plan": "basic"},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_stripe_payment_method():
    """Método de pago de ejemplo para tests"""
    return StripePaymentMethod(
        id="1",
        stripe_payment_method_id="pm_test123",
        stripe_customer_id="cus_test123",
        type="card",
        card_last4="4242",
        card_brand="visa",
        card_exp_month=12,
        card_exp_year=2025,
        is_default=True,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_stripe_transaction():
    """Transacción de ejemplo para tests"""
    return StripeTransaction(
        id="1",
        stripe_event_id="evt_test123",
        event_type=StripeEventType.PAYMENT_SUCCEEDED,
        object_id="pi_test123",
        amount=2000,
        currency="usd",
        status="succeeded",
        metadata={"invoice_id": "in_test123"},
        processed_at=datetime.now(),
        created_at=datetime.now()
    )


@pytest.fixture
def sample_stripe_price():
    """Precio de ejemplo para tests"""
    return StripePrice(
        id="1",
        stripe_price_id="price_test123",
        stripe_product_id="prod_test123",
        amount=1000,
        currency="usd",
        interval="month",
        interval_count=1,
        active=True,
        nickname="Basic Plan",
        metadata={"plan": "basic"},
        created_at=datetime.now()
    )


@pytest.fixture
def mock_db_session():
    """Mock de sesión de base de datos"""
    session = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    session.delete = Mock()
    session.execute = Mock()
    return session


@pytest.fixture
def sample_stripe_customer_data():
    """Datos de customer de Stripe API"""
    return {
        "id": "cus_test123",
        "email": "test@example.com",
        "name": "John Doe",
        "phone": "+1234567890",
        "metadata": {"user_id": "123"},
        "created": 1640995200
    }


@pytest.fixture
def sample_stripe_subscription_data():
    """Datos de suscripción de Stripe API"""
    return {
        "id": "sub_test123",
        "customer": "cus_test123",
        "status": "active",
        "current_period_start": 1640995200,
        "current_period_end": 1643673600,
        "cancel_at_period_end": False,
        "canceled_at": None,
        "trial_start": None,
        "trial_end": None,
        "metadata": {"plan": "basic"},
        "items": {
            "data": [
                {
                    "price": {
                        "id": "price_test123"
                    }
                }
            ]
        }
    }


@pytest.fixture
def sample_stripe_event_data():
    """Datos de evento de Stripe API"""
    return {
        "id": "evt_test123",
        "type": "customer.created",
        "data": {
            "object": {
                "id": "cus_test123",
                "email": "test@example.com"
            }
        },
        "created": 1640995200
    }


@pytest.fixture
def sample_stripe_price_data():
    """Datos de precio de Stripe API"""
    return {
        "id": "price_test123",
        "product": "prod_test123",
        "unit_amount": 1000,
        "currency": "usd",
        "recurring": {
            "interval": "month",
            "interval_count": 1
        },
        "active": True,
        "nickname": "Basic Plan",
        "metadata": {"plan": "basic"}
    }


@pytest.fixture
def sample_stripe_setup_intent_data():
    """Datos de setup intent de Stripe API"""
    return {
        "id": "seti_test123",
        "client_secret": "seti_test123_secret_abc123",
        "customer": "cus_test123",
        "payment_method_types": ["card"],
        "usage": "off_session"
    }


@pytest.fixture
def sample_stripe_payment_method_data():
    """Datos de método de pago de Stripe API"""
    return {
        "id": "pm_test123",
        "type": "card",
        "customer": "cus_test123",
        "card": {
            "last4": "4242",
            "brand": "visa",
            "exp_month": 12,
            "exp_year": 2025
        }
    }