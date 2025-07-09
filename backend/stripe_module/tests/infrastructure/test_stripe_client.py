import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from ...infrastructure.stripe_client.stripe_client import StripeClient
from ...infrastructure.config import StripeConfig


class TestStripeClient:
    """Tests para StripeClient"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock para configuración de Stripe"""
        config = Mock(spec=StripeConfig)
        config.stripe_secret_key = "sk_test_123"
        config.stripe_api_version = "2023-10-16"
        config.stripe_webhook_secret = "whsec_test123"
        return config
    
    @pytest.fixture
    def stripe_client(self, mock_config):
        """StripeClient con configuración mock"""
        return StripeClient(config=mock_config)
    
    @pytest.mark.asyncio
    async def test_create_customer_success(self, stripe_client):
        """Test crear customer exitosamente"""
        expected_customer = {
            "id": "cus_test123",
            "email": "test@example.com",
            "name": "John Doe"
        }
        
        with patch('stripe.Customer.create') as mock_create:
            mock_create.return_value = expected_customer
            
            result = await stripe_client.create_customer(
                email="test@example.com",
                name="John Doe"
            )
            
            mock_create.assert_called_once_with(
                email="test@example.com",
                name="John Doe"
            )
            assert result == expected_customer
    
    @pytest.mark.asyncio
    async def test_create_customer_minimal(self, stripe_client):
        """Test crear customer con datos mínimos"""
        expected_customer = {
            "id": "cus_test123",
            "email": "test@example.com"
        }
        
        with patch('stripe.Customer.create') as mock_create:
            mock_create.return_value = expected_customer
            
            result = await stripe_client.create_customer(
                email="test@example.com"
            )
            
            mock_create.assert_called_once_with(
                email="test@example.com"
            )
            assert result == expected_customer
    
    @pytest.mark.asyncio
    async def test_create_customer_error(self, stripe_client):
        """Test crear customer con error de Stripe"""
        with patch('stripe.Customer.create') as mock_create:
            mock_create.side_effect = Exception("Stripe API Error")
            
            with pytest.raises(ValueError, match="Error creating customer"):
                await stripe_client.create_customer(
                    email="test@example.com"
                )
    
    @pytest.mark.asyncio
    async def test_get_customer_success(self, stripe_client):
        """Test obtener customer exitosamente"""
        expected_customer = {
            "id": "cus_test123",
            "email": "test@example.com",
            "name": "John Doe"
        }
        
        with patch('stripe.Customer.retrieve') as mock_retrieve:
            mock_retrieve.return_value = expected_customer
            
            result = await stripe_client.get_customer("cus_test123")
            
            mock_retrieve.assert_called_once_with("cus_test123")
            assert result == expected_customer
    
    @pytest.mark.asyncio
    async def test_get_customer_error(self, stripe_client):
        """Test obtener customer con error"""
        with patch('stripe.Customer.retrieve') as mock_retrieve:
            mock_retrieve.side_effect = Exception("Customer not found")
            
            with pytest.raises(ValueError, match="Error retrieving customer"):
                await stripe_client.get_customer("cus_invalid")
    
    @pytest.mark.asyncio
    async def test_create_subscription_success(self, stripe_client):
        """Test crear suscripción exitosamente"""
        expected_subscription = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "active",
            "current_period_start": 1640995200,
            "current_period_end": 1643673600,
            "latest_invoice": {
                "payment_intent": {
                    "id": "pi_test123"
                }
            }
        }
        
        with patch('stripe.Subscription.create') as mock_create:
            mock_create.return_value = expected_subscription
            
            result = await stripe_client.create_subscription(
                customer_id="cus_test123",
                price_id="price_test123",
                payment_method_id="pm_test123"
            )
            
            mock_create.assert_called_once_with(
                customer="cus_test123",
                items=[{"price": "price_test123"}],
                payment_behavior="default_incomplete",
                payment_settings={
                    "save_default_payment_method": "on_subscription"
                },
                expand=["latest_invoice.payment_intent"],
                default_payment_method="pm_test123"
            )
            assert result == expected_subscription
    
    @pytest.mark.asyncio
    async def test_create_subscription_without_payment_method(self, stripe_client):
        """Test crear suscripción sin método de pago"""
        expected_subscription = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "incomplete"
        }
        
        with patch('stripe.Subscription.create') as mock_create:
            mock_create.return_value = expected_subscription
            
            result = await stripe_client.create_subscription(
                customer_id="cus_test123",
                price_id="price_test123"
            )
            
            # Verificar que se llamó sin default_payment_method
            call_args = mock_create.call_args[1]
            assert "default_payment_method" not in call_args
            assert call_args["customer"] == "cus_test123"
            assert call_args["items"] == [{"price": "price_test123"}]
            
            assert result == expected_subscription
    
    @pytest.mark.asyncio
    async def test_create_subscription_error(self, stripe_client):
        """Test crear suscripción con error"""
        with patch('stripe.Subscription.create') as mock_create:
            mock_create.side_effect = Exception("Subscription creation failed")
            
            with pytest.raises(ValueError, match="Error creating subscription"):
                await stripe_client.create_subscription(
                    customer_id="cus_test123",
                    price_id="price_test123"
                )
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_success(self, stripe_client):
        """Test cancelar suscripción exitosamente"""
        expected_subscription = {
            "id": "sub_test123",
            "status": "canceled",
            "canceled_at": 1640995200
        }
        
        with patch('stripe.Subscription.delete') as mock_delete:
            mock_delete.return_value = expected_subscription
            
            result = await stripe_client.cancel_subscription("sub_test123")
            
            mock_delete.assert_called_once_with("sub_test123")
            assert result == expected_subscription
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_error(self, stripe_client):
        """Test cancelar suscripción con error"""
        with patch('stripe.Subscription.delete') as mock_delete:
            mock_delete.side_effect = Exception("Subscription not found")
            
            with pytest.raises(ValueError, match="Error canceling subscription"):
                await stripe_client.cancel_subscription("sub_invalid")
    
    @pytest.mark.asyncio
    async def test_create_setup_intent_success(self, stripe_client):
        """Test crear setup intent exitosamente"""
        expected_setup_intent = {
            "id": "seti_test123",
            "client_secret": "seti_test123_secret_abc123",
            "customer": "cus_test123"
        }
        
        with patch('stripe.SetupIntent.create') as mock_create:
            mock_create.return_value = expected_setup_intent
            
            result = await stripe_client.create_setup_intent("cus_test123")
            
            mock_create.assert_called_once_with(
                customer="cus_test123",
                payment_method_types=["card"],
                usage="off_session"
            )
            assert result == expected_setup_intent
    
    @pytest.mark.asyncio
    async def test_create_setup_intent_error(self, stripe_client):
        """Test crear setup intent con error"""
        with patch('stripe.SetupIntent.create') as mock_create:
            mock_create.side_effect = Exception("Setup intent creation failed")
            
            with pytest.raises(ValueError, match="Error creating setup intent"):
                await stripe_client.create_setup_intent("cus_test123")
    
    @pytest.mark.asyncio
    async def test_get_payment_methods_success(self, stripe_client):
        """Test obtener métodos de pago exitosamente"""
        expected_payment_methods = {
            "data": [
                {
                    "id": "pm_test123",
                    "type": "card",
                    "card": {
                        "last4": "4242",
                        "brand": "visa"
                    }
                }
            ]
        }
        
        with patch('stripe.PaymentMethod.list') as mock_list:
            mock_list.return_value = expected_payment_methods
            
            result = await stripe_client.get_payment_methods("cus_test123")
            
            mock_list.assert_called_once_with(
                customer="cus_test123",
                type="card"
            )
            assert result == expected_payment_methods
    
    @pytest.mark.asyncio
    async def test_get_payment_methods_error(self, stripe_client):
        """Test obtener métodos de pago con error"""
        with patch('stripe.PaymentMethod.list') as mock_list:
            mock_list.side_effect = Exception("Payment methods retrieval failed")
            
            with pytest.raises(ValueError, match="Error retrieving payment methods"):
                await stripe_client.get_payment_methods("cus_test123")
    
    @pytest.mark.asyncio
    async def test_get_prices_success(self, stripe_client):
        """Test obtener precios exitosamente"""
        expected_prices = {
            "data": [
                {
                    "id": "price_test123",
                    "unit_amount": 1000,
                    "currency": "usd",
                    "recurring": {
                        "interval": "month"
                    }
                }
            ]
        }
        
        with patch('stripe.Price.list') as mock_list:
            mock_list.return_value = expected_prices
            
            result = await stripe_client.get_prices()
            
            mock_list.assert_called_once_with(active=True)
            assert result == expected_prices
    
    @pytest.mark.asyncio
    async def test_get_prices_error(self, stripe_client):
        """Test obtener precios con error"""
        with patch('stripe.Price.list') as mock_list:
            mock_list.side_effect = Exception("Prices retrieval failed")
            
            with pytest.raises(ValueError, match="Error retrieving prices"):
                await stripe_client.get_prices()
    
    def test_verify_webhook_signature_success(self, stripe_client):
        """Test verificar firma de webhook exitosamente"""
        payload = b'{"id": "evt_test123", "type": "customer.created"}'
        signature = "t=1640995200,v1=abc123"
        
        expected_event = {
            "id": "evt_test123",
            "type": "customer.created",
            "data": {
                "object": {
                    "id": "cus_test123"
                }
            }
        }
        
        with patch('stripe.Webhook.construct_event') as mock_construct:
            mock_construct.return_value = expected_event
            
            result = stripe_client.verify_webhook_signature(payload, signature)
            
            mock_construct.assert_called_once_with(
                payload,
                signature,
                stripe_client.config.stripe_webhook_secret
            )
            assert result == expected_event
    
    def test_verify_webhook_signature_invalid_payload(self, stripe_client):
        """Test verificar firma con payload inválido"""
        payload = b'invalid json'
        signature = "t=1640995200,v1=abc123"
        
        with patch('stripe.Webhook.construct_event') as mock_construct:
            mock_construct.side_effect = ValueError("Invalid payload")
            
            with pytest.raises(ValueError, match="Invalid payload"):
                stripe_client.verify_webhook_signature(payload, signature)
    
    def test_verify_webhook_signature_invalid_signature(self, stripe_client):
        """Test verificar firma inválida"""
        payload = b'{"id": "evt_test123", "type": "customer.created"}'
        signature = "invalid_signature"
        
        with patch('stripe.Webhook.construct_event') as mock_construct:
            from stripe.error import SignatureVerificationError
            mock_construct.side_effect = SignatureVerificationError("Invalid signature", "invalid_signature")
            
            with pytest.raises(ValueError, match="Invalid signature"):
                stripe_client.verify_webhook_signature(payload, signature)
    
    @pytest.mark.asyncio
    async def test_attach_payment_method_success(self, stripe_client):
        """Test asociar método de pago exitosamente"""
        expected_payment_method = {
            "id": "pm_test123",
            "customer": "cus_test123"
        }
        
        with patch('stripe.PaymentMethod.attach') as mock_attach:
            mock_attach.return_value = expected_payment_method
            
            result = await stripe_client.attach_payment_method("pm_test123", "cus_test123")
            
            mock_attach.assert_called_once_with(
                "pm_test123",
                customer="cus_test123"
            )
            assert result == expected_payment_method
    
    @pytest.mark.asyncio
    async def test_attach_payment_method_error(self, stripe_client):
        """Test asociar método de pago con error"""
        with patch('stripe.PaymentMethod.attach') as mock_attach:
            mock_attach.side_effect = Exception("Payment method attachment failed")
            
            with pytest.raises(ValueError, match="Error attaching payment method"):
                await stripe_client.attach_payment_method("pm_test123", "cus_test123")
    
    @pytest.mark.asyncio
    async def test_detach_payment_method_success(self, stripe_client):
        """Test desasociar método de pago exitosamente"""
        expected_payment_method = {
            "id": "pm_test123",
            "customer": None
        }
        
        with patch('stripe.PaymentMethod.detach') as mock_detach:
            mock_detach.return_value = expected_payment_method
            
            result = await stripe_client.detach_payment_method("pm_test123")
            
            mock_detach.assert_called_once_with("pm_test123")
            assert result == expected_payment_method
    
    @pytest.mark.asyncio
    async def test_detach_payment_method_error(self, stripe_client):
        """Test desasociar método de pago con error"""
        with patch('stripe.PaymentMethod.detach') as mock_detach:
            mock_detach.side_effect = Exception("Payment method detachment failed")
            
            with pytest.raises(ValueError, match="Error detaching payment method"):
                await stripe_client.detach_payment_method("pm_test123")
    
    @pytest.mark.asyncio
    async def test_update_customer_success(self, stripe_client):
        """Test actualizar customer exitosamente"""
        expected_customer = {
            "id": "cus_test123",
            "email": "updated@example.com",
            "name": "Updated Name"
        }
        
        with patch('stripe.Customer.modify') as mock_modify:
            mock_modify.return_value = expected_customer
            
            result = await stripe_client.update_customer(
                "cus_test123",
                email="updated@example.com",
                name="Updated Name"
            )
            
            mock_modify.assert_called_once_with(
                "cus_test123",
                email="updated@example.com",
                name="Updated Name"
            )
            assert result == expected_customer
    
    @pytest.mark.asyncio
    async def test_update_customer_error(self, stripe_client):
        """Test actualizar customer con error"""
        with patch('stripe.Customer.modify') as mock_modify:
            mock_modify.side_effect = Exception("Customer update failed")
            
            with pytest.raises(ValueError, match="Error updating customer"):
                await stripe_client.update_customer(
                    "cus_test123",
                    email="updated@example.com"
                )