import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from ...domain.services import StripeDomainService
from ...domain.entities import (
    StripeCustomer,
    StripeSubscription,
    StripePaymentMethod,
    StripeTransaction,
    StripePrice,
    StripeSubscriptionStatus,
    StripeEventType
)
from ...domain.repositories import (
    StripeService,
    StripeCustomerRepository,
    StripeSubscriptionRepository,
    StripePaymentMethodRepository,
    StripeTransactionRepository,
    StripePriceRepository
)


class TestStripeDomainService:
    """Tests para StripeDomainService"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeService"""
        mock = Mock(spec=StripeService)
        mock.create_customer = AsyncMock()
        mock.create_subscription = AsyncMock()
        mock.cancel_subscription = AsyncMock()
        mock.get_customer = AsyncMock()
        mock.get_subscription = AsyncMock()
        mock.get_prices = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_customer_repo(self):
        """Mock para StripeCustomerRepository"""
        mock = Mock(spec=StripeCustomerRepository)
        mock.create_customer = AsyncMock()
        mock.get_customer_by_stripe_id = AsyncMock()
        mock.update_customer = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_subscription_repo(self):
        """Mock para StripeSubscriptionRepository"""
        mock = Mock(spec=StripeSubscriptionRepository)
        mock.create_subscription = AsyncMock()
        mock.get_subscription_by_stripe_id = AsyncMock()
        mock.update_subscription = AsyncMock()
        mock.get_subscriptions_by_customer_id = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_payment_method_repo(self):
        """Mock para StripePaymentMethodRepository"""
        mock = Mock(spec=StripePaymentMethodRepository)
        mock.get_payment_methods_by_customer_id = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock para StripeTransactionRepository"""
        mock = Mock(spec=StripeTransactionRepository)
        mock.create_transaction = AsyncMock()
        mock.get_transaction_by_stripe_event_id = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_price_repo(self):
        """Mock para StripePriceRepository"""
        mock = Mock(spec=StripePriceRepository)
        mock.get_active_prices = AsyncMock()
        mock.get_price_by_stripe_id = AsyncMock()
        mock.create_price = AsyncMock()
        mock.update_price = AsyncMock()
        return mock
    
    @pytest.fixture
    def stripe_domain_service(self, mock_stripe_service, mock_customer_repo, mock_subscription_repo, 
                             mock_payment_method_repo, mock_transaction_repo, mock_price_repo):
        """StripeDomainService con mocks"""
        return StripeDomainService(
            stripe_service=mock_stripe_service,
            customer_repo=mock_customer_repo,
            subscription_repo=mock_subscription_repo,
            payment_method_repo=mock_payment_method_repo,
            transaction_repo=mock_transaction_repo,
            price_repo=mock_price_repo
        )
    
    @pytest.mark.asyncio
    async def test_create_customer_with_sync(self, stripe_domain_service, mock_stripe_service, mock_customer_repo):
        """Test crear customer con sincronización"""
        # Preparar mocks
        stripe_customer_data = {
            "id": "cus_test123",
            "email": "test@example.com",
            "metadata": {}
        }
        mock_stripe_service.create_customer.return_value = stripe_customer_data
        
        created_customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="test@example.com",
            name="John Doe",
            metadata={}
        )
        mock_customer_repo.create_customer.return_value = created_customer
        
        # Ejecutar
        result = await stripe_domain_service.create_customer_with_sync(
            email="test@example.com",
            name="John Doe"
        )
        
        # Verificar
        mock_stripe_service.create_customer.assert_called_once_with("test@example.com", "John Doe")
        mock_customer_repo.create_customer.assert_called_once()
        
        # Verificar el customer creado
        created_customer_arg = mock_customer_repo.create_customer.call_args[0][0]
        assert created_customer_arg.stripe_customer_id == "cus_test123"
        assert created_customer_arg.email == "test@example.com"
        assert created_customer_arg.name == "John Doe"
        
        assert result == created_customer
    
    @pytest.mark.asyncio
    async def test_create_subscription_with_sync(self, stripe_domain_service, mock_stripe_service, mock_subscription_repo):
        """Test crear suscripción con sincronización"""
        # Preparar mocks
        stripe_subscription_data = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "active",
            "current_period_start": 1640995200,  # timestamp
            "current_period_end": 1643673600,    # timestamp
            "cancel_at_period_end": False,
            "trial_start": None,
            "trial_end": None,
            "metadata": {}
        }
        mock_stripe_service.create_subscription.return_value = stripe_subscription_data
        
        created_subscription = StripeSubscription(
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.ACTIVE,
            current_period_start=datetime.fromtimestamp(1640995200),
            current_period_end=datetime.fromtimestamp(1643673600),
            cancel_at_period_end=False,
            metadata={}
        )
        mock_subscription_repo.create_subscription.return_value = created_subscription
        
        # Ejecutar
        result = await stripe_domain_service.create_subscription_with_sync(
            customer_id="cus_test123",
            price_id="price_test123",
            payment_method_id="pm_test123"
        )
        
        # Verificar
        mock_stripe_service.create_subscription.assert_called_once_with(
            "cus_test123", "price_test123", "pm_test123"
        )
        mock_subscription_repo.create_subscription.assert_called_once()
        
        # Verificar la suscripción creada
        created_subscription_arg = mock_subscription_repo.create_subscription.call_args[0][0]
        assert created_subscription_arg.stripe_subscription_id == "sub_test123"
        assert created_subscription_arg.stripe_customer_id == "cus_test123"
        assert created_subscription_arg.stripe_price_id == "price_test123"
        assert created_subscription_arg.status == StripeSubscriptionStatus.ACTIVE
        
        assert result == created_subscription
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_with_sync(self, stripe_domain_service, mock_stripe_service, mock_subscription_repo):
        """Test cancelar suscripción con sincronización"""
        # Preparar mocks
        existing_subscription = StripeSubscription(
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.ACTIVE,
            current_period_start=datetime.now(),
            current_period_end=datetime.now(),
            cancel_at_period_end=False
        )
        mock_subscription_repo.get_subscription_by_stripe_id.return_value = existing_subscription
        
        stripe_subscription_data = {
            "id": "sub_test123",
            "status": "canceled",
            "canceled_at": 1640995200,
            "cancel_at_period_end": True
        }
        mock_stripe_service.cancel_subscription.return_value = stripe_subscription_data
        
        updated_subscription = StripeSubscription(
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.CANCELED,
            current_period_start=datetime.now(),
            current_period_end=datetime.now(),
            cancel_at_period_end=True,
            canceled_at=datetime.fromtimestamp(1640995200)
        )
        mock_subscription_repo.update_subscription.return_value = updated_subscription
        
        # Ejecutar
        result = await stripe_domain_service.cancel_subscription_with_sync("sub_test123")
        
        # Verificar
        mock_stripe_service.cancel_subscription.assert_called_once_with("sub_test123")
        mock_subscription_repo.get_subscription_by_stripe_id.assert_called_once_with("sub_test123")
        mock_subscription_repo.update_subscription.assert_called_once()
        
        # Verificar la suscripción actualizada
        updated_subscription_arg = mock_subscription_repo.update_subscription.call_args[0][0]
        assert updated_subscription_arg.status == StripeSubscriptionStatus.CANCELED
        assert updated_subscription_arg.cancel_at_period_end is True
        
        assert result == updated_subscription
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_not_found(self, stripe_domain_service, mock_subscription_repo):
        """Test cancelar suscripción que no existe"""
        # Preparar mocks
        mock_subscription_repo.get_subscription_by_stripe_id.return_value = None
        
        # Ejecutar y verificar excepción
        with pytest.raises(ValueError, match="Subscription not found in local database"):
            await stripe_domain_service.cancel_subscription_with_sync("sub_test123")
    
    @pytest.mark.asyncio
    async def test_sync_customer_from_stripe_existing(self, stripe_domain_service, mock_stripe_service, mock_customer_repo):
        """Test sincronizar customer existente desde Stripe"""
        # Preparar mocks
        stripe_customer_data = {
            "id": "cus_test123",
            "email": "updated@example.com",
            "name": "Updated Name",
            "phone": "+1234567890",
            "metadata": {"updated": True}
        }
        mock_stripe_service.get_customer.return_value = stripe_customer_data
        
        existing_customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="old@example.com",
            name="Old Name"
        )
        mock_customer_repo.get_customer_by_stripe_id.return_value = existing_customer
        
        updated_customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="updated@example.com",
            name="Updated Name",
            phone="+1234567890",
            metadata={"updated": True}
        )
        mock_customer_repo.update_customer.return_value = updated_customer
        
        # Ejecutar
        result = await stripe_domain_service.sync_customer_from_stripe("cus_test123")
        
        # Verificar
        mock_stripe_service.get_customer.assert_called_once_with("cus_test123")
        mock_customer_repo.get_customer_by_stripe_id.assert_called_once_with("cus_test123")
        mock_customer_repo.update_customer.assert_called_once()
        
        # Verificar datos actualizados
        updated_customer_arg = mock_customer_repo.update_customer.call_args[0][0]
        assert updated_customer_arg.email == "updated@example.com"
        assert updated_customer_arg.name == "Updated Name"
        assert updated_customer_arg.phone == "+1234567890"
        assert updated_customer_arg.metadata == {"updated": True}
        
        assert result == updated_customer
    
    @pytest.mark.asyncio
    async def test_sync_customer_from_stripe_new(self, stripe_domain_service, mock_stripe_service, mock_customer_repo):
        """Test sincronizar customer nuevo desde Stripe"""
        # Preparar mocks
        stripe_customer_data = {
            "id": "cus_test123",
            "email": "new@example.com",
            "name": "New Name",
            "phone": None,
            "metadata": {}
        }
        mock_stripe_service.get_customer.return_value = stripe_customer_data
        
        # Customer no existe localmente
        mock_customer_repo.get_customer_by_stripe_id.return_value = None
        
        new_customer = StripeCustomer(
            stripe_customer_id="cus_test123",
            email="new@example.com",
            name="New Name",
            phone=None,
            metadata={}
        )
        mock_customer_repo.create_customer.return_value = new_customer
        
        # Ejecutar
        result = await stripe_domain_service.sync_customer_from_stripe("cus_test123")
        
        # Verificar
        mock_stripe_service.get_customer.assert_called_once_with("cus_test123")
        mock_customer_repo.get_customer_by_stripe_id.assert_called_once_with("cus_test123")
        mock_customer_repo.create_customer.assert_called_once()
        
        # Verificar customer creado
        created_customer_arg = mock_customer_repo.create_customer.call_args[0][0]
        assert created_customer_arg.stripe_customer_id == "cus_test123"
        assert created_customer_arg.email == "new@example.com"
        assert created_customer_arg.name == "New Name"
        
        assert result == new_customer
    
    @pytest.mark.asyncio
    async def test_process_stripe_event_existing(self, stripe_domain_service, mock_transaction_repo):
        """Test procesar evento de Stripe ya procesado"""
        # Preparar mocks
        existing_transaction = StripeTransaction(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            status="processed"
        )
        mock_transaction_repo.get_transaction_by_stripe_event_id.return_value = existing_transaction
        
        event_data = {
            "id": "evt_test123",
            "type": "customer.created",
            "data": {
                "object": {
                    "id": "cus_test123"
                }
            }
        }
        
        # Ejecutar
        result = await stripe_domain_service.process_stripe_event(event_data)
        
        # Verificar
        mock_transaction_repo.get_transaction_by_stripe_event_id.assert_called_once_with("evt_test123")
        assert result == existing_transaction
    
    @pytest.mark.asyncio
    async def test_process_stripe_event_new(self, stripe_domain_service, mock_transaction_repo):
        """Test procesar evento de Stripe nuevo"""
        # Preparar mocks
        mock_transaction_repo.get_transaction_by_stripe_event_id.return_value = None
        
        new_transaction = StripeTransaction(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            status="processed"
        )
        mock_transaction_repo.create_transaction.return_value = new_transaction
        
        event_data = {
            "id": "evt_test123",
            "type": "customer.created",
            "data": {
                "object": {
                    "id": "cus_test123"
                }
            }
        }
        
        # Ejecutar
        result = await stripe_domain_service.process_stripe_event(event_data)
        
        # Verificar
        mock_transaction_repo.get_transaction_by_stripe_event_id.assert_called_once_with("evt_test123")
        mock_transaction_repo.create_transaction.assert_called_once()
        
        # Verificar transacción creada
        created_transaction_arg = mock_transaction_repo.create_transaction.call_args[0][0]
        assert created_transaction_arg.stripe_event_id == "evt_test123"
        assert created_transaction_arg.event_type == StripeEventType.CUSTOMER_CREATED
        assert created_transaction_arg.object_id == "cus_test123"
        assert created_transaction_arg.status == "processed"
        
        assert result == new_transaction
    
    @pytest.mark.asyncio
    async def test_get_customer_subscriptions(self, stripe_domain_service, mock_subscription_repo):
        """Test obtener suscripciones de customer"""
        # Preparar mocks
        subscriptions = [
            StripeSubscription(
                stripe_subscription_id="sub_test123",
                stripe_customer_id="cus_test123",
                stripe_price_id="price_test123",
                status=StripeSubscriptionStatus.ACTIVE,
                current_period_start=datetime.now(),
                current_period_end=datetime.now()
            ),
            StripeSubscription(
                stripe_subscription_id="sub_test456",
                stripe_customer_id="cus_test123",
                stripe_price_id="price_test456",
                status=StripeSubscriptionStatus.CANCELED,
                current_period_start=datetime.now(),
                current_period_end=datetime.now()
            )
        ]
        mock_subscription_repo.get_subscriptions_by_customer_id.return_value = subscriptions
        
        # Ejecutar
        result = await stripe_domain_service.get_customer_subscriptions("cus_test123")
        
        # Verificar
        mock_subscription_repo.get_subscriptions_by_customer_id.assert_called_once_with("cus_test123")
        assert result == subscriptions
    
    @pytest.mark.asyncio
    async def test_get_active_prices(self, stripe_domain_service, mock_price_repo):
        """Test obtener precios activos"""
        # Preparar mocks
        prices = [
            StripePrice(
                stripe_price_id="price_test123",
                stripe_product_id="prod_test123",
                amount=1000,
                currency="usd",
                interval="month",
                active=True
            ),
            StripePrice(
                stripe_price_id="price_test456",
                stripe_product_id="prod_test456",
                amount=2000,
                currency="usd",
                interval="month",
                active=True
            )
        ]
        mock_price_repo.get_active_prices.return_value = prices
        
        # Ejecutar
        result = await stripe_domain_service.get_active_prices()
        
        # Verificar
        mock_price_repo.get_active_prices.assert_called_once()
        assert result == prices
    
    @pytest.mark.asyncio
    async def test_sync_prices_from_stripe(self, stripe_domain_service, mock_stripe_service, mock_price_repo):
        """Test sincronizar precios desde Stripe"""
        # Preparar mocks
        stripe_prices_data = {
            "data": [
                {
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
                },
                {
                    "id": "price_test456",
                    "product": "prod_test456",
                    "unit_amount": 2000,
                    "currency": "usd",
                    "recurring": {
                        "interval": "month",
                        "interval_count": 1
                    },
                    "active": True,
                    "nickname": "Premium Plan",
                    "metadata": {"plan": "premium"}
                }
            ]
        }
        mock_stripe_service.get_prices.return_value = stripe_prices_data
        
        # Precios no existen localmente
        mock_price_repo.get_price_by_stripe_id.return_value = None
        
        synced_prices = [
            StripePrice(
                stripe_price_id="price_test123",
                stripe_product_id="prod_test123",
                amount=1000,
                currency="usd",
                interval="month",
                interval_count=1,
                active=True,
                nickname="Basic Plan",
                metadata={"plan": "basic"}
            ),
            StripePrice(
                stripe_price_id="price_test456",
                stripe_product_id="prod_test456",
                amount=2000,
                currency="usd",
                interval="month",
                interval_count=1,
                active=True,
                nickname="Premium Plan",
                metadata={"plan": "premium"}
            )
        ]
        mock_price_repo.create_price.side_effect = synced_prices
        
        # Ejecutar
        result = await stripe_domain_service.sync_prices_from_stripe()
        
        # Verificar
        mock_stripe_service.get_prices.assert_called_once()
        assert mock_price_repo.create_price.call_count == 2
        assert len(result) == 2
        assert result[0].stripe_price_id == "price_test123"
        assert result[1].stripe_price_id == "price_test456"