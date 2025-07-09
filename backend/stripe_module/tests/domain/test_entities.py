import pytest
from datetime import datetime
from typing import Dict, Any

from ...domain.entities import (
    StripeCustomer,
    StripeSubscription,
    StripePaymentMethod,
    StripeTransaction,
    StripePrice,
    StripeSubscriptionStatus,
    StripeEventType
)


class TestStripeCustomer:
    """Tests para la entidad StripeCustomer"""
    
    def test_create_customer_with_minimal_data(self):
        """Test crear customer con datos mínimos"""
        customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="test@example.com"
        )
        
        assert customer.stripe_customer_id == "cus_test123"
        assert customer.email == "test@example.com"
        assert customer.name is None
        assert customer.phone is None
        assert customer.metadata is None
        assert customer.created_at is None
        assert customer.id is None
    
    def test_create_customer_with_full_data(self):
        """Test crear customer con todos los datos"""
        metadata = {"user_id": "123", "plan": "basic"}
        created_at = datetime.now()
        
        customer = StripeCustomer(
            id="1",
            stripe_customer_id="cus_test123",
            email="test@example.com",
            name="John Doe",
            phone="+1234567890",
            metadata=metadata,
            created_at=created_at
        )
        
        assert customer.id == "1"
        assert customer.stripe_customer_id == "cus_test123"
        assert customer.email == "test@example.com"
        assert customer.name == "John Doe"
        assert customer.phone == "+1234567890"
        assert customer.metadata == metadata
        assert customer.created_at == created_at
    
    def test_customer_validation(self):
        """Test validación de customer"""
        # Test email requerido
        with pytest.raises(ValueError):
            StripeCustomer(stripe_customer_id="cus_test123")
        
        # Test stripe_customer_id requerido
        with pytest.raises(ValueError):
            StripeCustomer(email="test@example.com")


class TestStripeSubscription:
    """Tests para la entidad StripeSubscription"""
    
    def test_create_subscription_with_minimal_data(self):
        """Test crear suscripción con datos mínimos"""
        period_start = datetime.now()
        period_end = datetime.now()
        
        subscription = StripeSubscription(
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.ACTIVE,
            current_period_start=period_start,
            current_period_end=period_end
        )
        
        assert subscription.stripe_subscription_id == "sub_test123"
        assert subscription.stripe_customer_id == "cus_test123"
        assert subscription.stripe_price_id == "price_test123"
        assert subscription.status == StripeSubscriptionStatus.ACTIVE
        assert subscription.current_period_start == period_start
        assert subscription.current_period_end == period_end
        assert subscription.cancel_at_period_end is False
        assert subscription.canceled_at is None
        assert subscription.trial_start is None
        assert subscription.trial_end is None
        assert subscription.metadata is None
    
    def test_create_subscription_with_full_data(self):
        """Test crear suscripción con todos los datos"""
        period_start = datetime.now()
        period_end = datetime.now()
        canceled_at = datetime.now()
        trial_start = datetime.now()
        trial_end = datetime.now()
        created_at = datetime.now()
        updated_at = datetime.now()
        metadata = {"plan": "premium"}
        
        subscription = StripeSubscription(
            id="1",
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.CANCELED,
            current_period_start=period_start,
            current_period_end=period_end,
            cancel_at_period_end=True,
            canceled_at=canceled_at,
            trial_start=trial_start,
            trial_end=trial_end,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at
        )
        
        assert subscription.id == "1"
        assert subscription.cancel_at_period_end is True
        assert subscription.canceled_at == canceled_at
        assert subscription.trial_start == trial_start
        assert subscription.trial_end == trial_end
        assert subscription.metadata == metadata
        assert subscription.created_at == created_at
        assert subscription.updated_at == updated_at
    
    def test_subscription_status_enum(self):
        """Test enum de estado de suscripción"""
        assert StripeSubscriptionStatus.ACTIVE == "active"
        assert StripeSubscriptionStatus.CANCELED == "canceled"
        assert StripeSubscriptionStatus.INCOMPLETE == "incomplete"
        assert StripeSubscriptionStatus.PAST_DUE == "past_due"
        assert StripeSubscriptionStatus.TRIALING == "trialing"
        assert StripeSubscriptionStatus.UNPAID == "unpaid"


class TestStripePaymentMethod:
    """Tests para la entidad StripePaymentMethod"""
    
    def test_create_payment_method_with_minimal_data(self):
        """Test crear método de pago con datos mínimos"""
        payment_method = StripePaymentMethod(
            stripe_payment_method_id="pm_test123",
            stripe_customer_id="cus_test123",
            type="card"
        )
        
        assert payment_method.stripe_payment_method_id == "pm_test123"
        assert payment_method.stripe_customer_id == "cus_test123"
        assert payment_method.type == "card"
        assert payment_method.card_last4 is None
        assert payment_method.card_brand is None
        assert payment_method.card_exp_month is None
        assert payment_method.card_exp_year is None
        assert payment_method.is_default is False
        assert payment_method.created_at is None
    
    def test_create_payment_method_with_card_data(self):
        """Test crear método de pago con datos de tarjeta"""
        created_at = datetime.now()
        
        payment_method = StripePaymentMethod(
            id="1",
            stripe_payment_method_id="pm_test123",
            stripe_customer_id="cus_test123",
            type="card",
            card_last4="4242",
            card_brand="visa",
            card_exp_month=12,
            card_exp_year=2025,
            is_default=True,
            created_at=created_at
        )
        
        assert payment_method.id == "1"
        assert payment_method.card_last4 == "4242"
        assert payment_method.card_brand == "visa"
        assert payment_method.card_exp_month == 12
        assert payment_method.card_exp_year == 2025
        assert payment_method.is_default is True
        assert payment_method.created_at == created_at


class TestStripeTransaction:
    """Tests para la entidad StripeTransaction"""
    
    def test_create_transaction_with_minimal_data(self):
        """Test crear transacción con datos mínimos"""
        occurred_at = datetime.now()
        
        transaction = StripeTransaction(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.INVOICE_PAYMENT_SUCCEEDED,
            object_id="pi_test123",
            status="succeeded"
        )
        
        assert transaction.stripe_event_id == "evt_test123"
        assert transaction.event_type == StripeEventType.INVOICE_PAYMENT_SUCCEEDED
        assert transaction.object_id == "pi_test123"
        assert transaction.status == "succeeded"
        assert transaction.amount is None
        assert transaction.currency is None
        assert transaction.metadata is None
        assert transaction.processed_at is None
        assert transaction.created_at is None
    
    def test_create_transaction_with_full_data(self):
        """Test crear transacción con todos los datos"""
        processed_at = datetime.now()
        created_at = datetime.now()
        metadata = {"invoice_id": "in_test123"}
        
        transaction = StripeTransaction(
            id="1",
            stripe_event_id="evt_test123",
            event_type=StripeEventType.INVOICE_PAYMENT_SUCCEEDED,
            object_id="in_test123",
            amount=2000,
            currency="usd",
            status="succeeded",
            metadata=metadata,
            processed_at=processed_at,
            created_at=created_at
        )
        
        assert transaction.id == "1"
        assert transaction.amount == 2000
        assert transaction.currency == "usd"
        assert transaction.metadata == metadata
        assert transaction.processed_at == processed_at
        assert transaction.created_at == created_at
    
    def test_event_type_enum(self):
        """Test enum de tipos de evento"""
        assert StripeEventType.CUSTOMER_CREATED == "customer.created"
        assert StripeEventType.SUBSCRIPTION_CREATED == "customer.subscription.created"
        assert StripeEventType.INVOICE_PAYMENT_SUCCEEDED == "invoice.payment_succeeded"
        assert StripeEventType.INVOICE_PAYMENT_FAILED == "invoice.payment_failed"


class TestStripePrice:
    """Tests para la entidad StripePrice"""
    
    def test_create_price_with_minimal_data(self):
        """Test crear precio con datos mínimos"""
        price = StripePrice(
            stripe_price_id="price_test123",
            stripe_product_id="prod_test123",
            amount=1000,
            currency="usd",
            interval="month"
        )
        
        assert price.stripe_price_id == "price_test123"
        assert price.stripe_product_id == "prod_test123"
        assert price.amount == 1000
        assert price.currency == "usd"
        assert price.interval == "month"
        assert price.interval_count == 1
        assert price.active is True
        assert price.nickname is None
        assert price.metadata is None
        assert price.created_at is None
    
    def test_create_price_with_full_data(self):
        """Test crear precio con todos los datos"""
        created_at = datetime.now()
        metadata = {"plan": "basic"}
        
        price = StripePrice(
            id="1",
            stripe_price_id="price_test123",
            stripe_product_id="prod_test123",
            amount=2000,
            currency="usd",
            interval="month",
            interval_count=1,
            active=True,
            nickname="Basic Plan",
            metadata=metadata,
            created_at=created_at
        )
        
        assert price.id == "1"
        assert price.nickname == "Basic Plan"
        assert price.metadata == metadata
        assert price.created_at == created_at
    
    def test_price_validation(self):
        """Test validación de precio"""
        # Test campos requeridos - missing stripe_price_id
        with pytest.raises(ValueError):
            StripePrice(
                stripe_product_id="prod_test123",
                amount=1000,
                currency="usd",
                interval="month"
            )
        
        # Test crear precio válido
        price = StripePrice(
            stripe_price_id="price_test123",
            stripe_product_id="prod_test123",
            amount=1000,
            currency="usd",
            interval="month"
        )
        assert price.stripe_price_id == "price_test123"
        assert price.amount == 1000


class TestEntitySerialization:
    """Tests para serialización de entidades"""
    
    def test_customer_to_dict(self):
        """Test serialización de customer a dict"""
        customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="test@example.com",
            name="John Doe"
        )
        
        data = customer.model_dump()
        assert data["stripe_customer_id"] == "cus_test123"
        assert data["email"] == "test@example.com"
        assert data["name"] == "John Doe"
    
    def test_subscription_to_dict(self):
        """Test serialización de suscripción a dict"""
        period_start = datetime.now()
        period_end = datetime.now()
        
        subscription = StripeSubscription(
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.ACTIVE,
            current_period_start=period_start,
            current_period_end=period_end
        )
        
        data = subscription.model_dump()
        assert data["stripe_subscription_id"] == "sub_test123"
        assert data["status"] == "active"  # Enum se serializa como string
    
    def test_customer_from_dict(self):
        """Test deserialización de customer desde dict"""
        data = {
            "stripe_customer_id": "cus_test123",
            "email": "test@example.com",
            "name": "John Doe"
        }
        
        customer = StripeCustomer(**data)
        assert customer.stripe_customer_id == "cus_test123"
        assert customer.email == "test@example.com"
        assert customer.name == "John Doe"