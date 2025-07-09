import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from ...application.use_cases import (
    CreateStripeCustomerUseCase,
    CreateStripeSubscriptionUseCase,
    CancelStripeSubscriptionUseCase,
    SetupStripePaymentMethodUseCase,
    GetStripeCustomerSubscriptionsUseCase,
    ProcessStripeWebhookUseCase
)
from ...application.dto import (
    CreateStripeCustomerDTO,
    CreateStripeSubscriptionDTO,
    CancelStripeSubscriptionDTO,
    SetupStripePaymentMethodDTO,
    GetStripeCustomerSubscriptionsDTO,
    ProcessStripeWebhookDTO
)
from ...domain.entities import (
    StripeCustomer,
    StripeSubscription,
    StripeTransaction,
    StripeSubscriptionStatus,
    StripeEventType
)
from ...domain.services import StripeDomainService
from ...domain.events import StripeEventPublisher


class TestCreateStripeCustomerUseCase:
    """Tests para CreateStripeCustomerUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.create_customer_with_sync = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_event_publisher(self):
        """Mock para StripeEventPublisher"""
        mock = Mock(spec=StripeEventPublisher)
        mock.publish_customer_created = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service, mock_event_publisher):
        """CreateStripeCustomerUseCase con mocks"""
        return CreateStripeCustomerUseCase(
            stripe_service=mock_stripe_service,
            event_publisher=mock_event_publisher
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service, mock_event_publisher):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = CreateStripeCustomerDTO(
            email="test@example.com",
            name="John Doe",
            phone="+1234567890",
            metadata={"user_id": "123"}
        )
        
        created_customer = StripeCustomer(
            id="1",
            stripe_customer_id="cus_test123",
            email="test@example.com",
            name="John Doe",
            phone="+1234567890",
            metadata={"user_id": "123"},
            created_at=datetime.now()
        )
        
        mock_stripe_service.create_customer_with_sync.return_value = created_customer
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.create_customer_with_sync.assert_called_once_with(
            email="test@example.com",
            name="John Doe"
        )
        
        mock_event_publisher.publish_customer_created.assert_called_once_with(
            customer_id="cus_test123",
            email="test@example.com",
            metadata={"user_id": "123"}
        )
        
        assert result.stripe_customer_id == "cus_test123"
        assert result.email == "test@example.com"
        assert result.name == "John Doe"
        assert result.phone == "+1234567890"
        assert result.metadata == {"user_id": "123"}
    
    @pytest.mark.asyncio
    async def test_execute_minimal_data(self, use_case, mock_stripe_service, mock_event_publisher):
        """Test ejecutar con datos mínimos"""
        # Preparar datos
        request = CreateStripeCustomerDTO(
            email="test@example.com"
        )
        
        created_customer = StripeCustomer(
            id="1",
            stripe_customer_id="cus_test123",
            email="test@example.com",
            name=None,
            phone=None,
            metadata=None,
            created_at=datetime.now()
        )
        
        mock_stripe_service.create_customer_with_sync.return_value = created_customer
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.create_customer_with_sync.assert_called_once_with(
            email="test@example.com",
            name=None
        )
        
        mock_event_publisher.publish_customer_created.assert_called_once_with(
            customer_id="cus_test123",
            email="test@example.com",
            metadata={}
        )
        
        assert result.stripe_customer_id == "cus_test123"
        assert result.email == "test@example.com"
        assert result.name is None


class TestCreateStripeSubscriptionUseCase:
    """Tests para CreateStripeSubscriptionUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.create_subscription_with_sync = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_event_publisher(self):
        """Mock para StripeEventPublisher"""
        mock = Mock(spec=StripeEventPublisher)
        mock.publish_subscription_created = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service, mock_event_publisher):
        """CreateStripeSubscriptionUseCase con mocks"""
        return CreateStripeSubscriptionUseCase(
            stripe_service=mock_stripe_service,
            event_publisher=mock_event_publisher
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service, mock_event_publisher):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = CreateStripeSubscriptionDTO(
            customer_id="cus_test123",
            price_id="price_test123",
            payment_method_id="pm_test123",
            trial_period_days=7,
            metadata={"plan": "basic"}
        )
        
        created_subscription = StripeSubscription(
            id="1",
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.ACTIVE,
            current_period_start=datetime.now(),
            current_period_end=datetime.now(),
            cancel_at_period_end=False,
            metadata={"plan": "basic"},
            created_at=datetime.now()
        )
        
        mock_stripe_service.create_subscription_with_sync.return_value = created_subscription
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.create_subscription_with_sync.assert_called_once_with(
            customer_id="cus_test123",
            price_id="price_test123",
            payment_method_id="pm_test123",
            trial_period_days=7
        )
        
        mock_event_publisher.publish_subscription_created.assert_called_once_with(
            subscription_id="sub_test123",
            customer_id="cus_test123",
            price_id="price_test123",
            metadata={"plan": "basic"}
        )
        
        assert result.stripe_subscription_id == "sub_test123"
        assert result.stripe_customer_id == "cus_test123"
        assert result.stripe_price_id == "price_test123"
        assert result.status == StripeSubscriptionStatus.ACTIVE
        assert result.metadata == {"plan": "basic"}


class TestCancelStripeSubscriptionUseCase:
    """Tests para CancelStripeSubscriptionUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.cancel_subscription_with_sync = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_event_publisher(self):
        """Mock para StripeEventPublisher"""
        mock = Mock(spec=StripeEventPublisher)
        mock.publish_subscription_canceled = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service, mock_event_publisher):
        """CancelStripeSubscriptionUseCase con mocks"""
        return CancelStripeSubscriptionUseCase(
            stripe_service=mock_stripe_service,
            event_publisher=mock_event_publisher
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service, mock_event_publisher):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = CancelStripeSubscriptionDTO(
            subscription_id="sub_test123",
            immediately=False
        )
        
        canceled_subscription = StripeSubscription(
            id="1",
            stripe_subscription_id="sub_test123",
            stripe_customer_id="cus_test123",
            stripe_price_id="price_test123",
            status=StripeSubscriptionStatus.CANCELED,
            current_period_start=datetime.now(),
            current_period_end=datetime.now(),
            cancel_at_period_end=True,
            canceled_at=datetime.now(),
            created_at=datetime.now()
        )
        
        mock_stripe_service.cancel_subscription_with_sync.return_value = canceled_subscription
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.cancel_subscription_with_sync.assert_called_once_with(
            subscription_id="sub_test123"
        )
        
        mock_event_publisher.publish_subscription_canceled.assert_called_once_with(
            subscription_id="sub_test123",
            customer_id="cus_test123"
        )
        
        assert result.stripe_subscription_id == "sub_test123"
        assert result.status == StripeSubscriptionStatus.CANCELED
        assert result.cancel_at_period_end is True
        assert result.canceled_at is not None


class TestSetupStripePaymentMethodUseCase:
    """Tests para SetupStripePaymentMethodUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.stripe_service = Mock()
        mock.stripe_service.create_setup_intent = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service):
        """SetupStripePaymentMethodUseCase con mocks"""
        return SetupStripePaymentMethodUseCase(
            stripe_service=mock_stripe_service
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = SetupStripePaymentMethodDTO(
            customer_id="cus_test123",
            usage="off_session",
            payment_method_types=["card"]
        )
        
        setup_intent = {
            "id": "seti_test123",
            "client_secret": "seti_test123_secret_abc123",
            "customer": "cus_test123"
        }
        
        mock_stripe_service.stripe_service.create_setup_intent.return_value = setup_intent
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.stripe_service.create_setup_intent.assert_called_once_with(
            customer_id="cus_test123"
        )
        
        assert result.client_secret == "seti_test123_secret_abc123"
        assert result.customer_id == "cus_test123"
        assert result.setup_intent_id == "seti_test123"


class TestGetStripeCustomerSubscriptionsUseCase:
    """Tests para GetStripeCustomerSubscriptionsUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.get_customer_subscriptions = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service):
        """GetStripeCustomerSubscriptionsUseCase con mocks"""
        return GetStripeCustomerSubscriptionsUseCase(
            stripe_service=mock_stripe_service
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = GetStripeCustomerSubscriptionsDTO(
            customer_id="cus_test123"
        )
        
        subscriptions = [
            StripeSubscription(
                id="1",
                stripe_subscription_id="sub_test123",
                stripe_customer_id="cus_test123",
                stripe_price_id="price_test123",
                status=StripeSubscriptionStatus.ACTIVE,
                current_period_start=datetime.now(),
                current_period_end=datetime.now(),
                cancel_at_period_end=False,
                created_at=datetime.now()
            ),
            StripeSubscription(
                id="2",
                stripe_subscription_id="sub_test456",
                stripe_customer_id="cus_test123",
                stripe_price_id="price_test456",
                status=StripeSubscriptionStatus.CANCELED,
                current_period_start=datetime.now(),
                current_period_end=datetime.now(),
                cancel_at_period_end=True,
                canceled_at=datetime.now(),
                created_at=datetime.now()
            )
        ]
        
        mock_stripe_service.get_customer_subscriptions.return_value = subscriptions
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.get_customer_subscriptions.assert_called_once_with("cus_test123")
        
        assert len(result) == 2
        assert result[0].stripe_subscription_id == "sub_test123"
        assert result[0].status == StripeSubscriptionStatus.ACTIVE
        assert result[1].stripe_subscription_id == "sub_test456"
        assert result[1].status == StripeSubscriptionStatus.CANCELED
    
    @pytest.mark.asyncio
    async def test_execute_no_subscriptions(self, use_case, mock_stripe_service):
        """Test ejecutar sin suscripciones"""
        # Preparar datos
        request = GetStripeCustomerSubscriptionsDTO(
            customer_id="cus_test123"
        )
        
        mock_stripe_service.get_customer_subscriptions.return_value = []
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.get_customer_subscriptions.assert_called_once_with("cus_test123")
        assert len(result) == 0


class TestProcessStripeWebhookUseCase:
    """Tests para ProcessStripeWebhookUseCase"""
    
    @pytest.fixture
    def mock_stripe_service(self):
        """Mock para StripeDomainService"""
        mock = Mock(spec=StripeDomainService)
        mock.stripe_service = Mock()
        mock.stripe_service.verify_webhook_signature = Mock()
        mock.process_stripe_event = AsyncMock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_stripe_service):
        """ProcessStripeWebhookUseCase con mocks"""
        return ProcessStripeWebhookUseCase(
            stripe_service=mock_stripe_service
        )
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_stripe_service):
        """Test ejecutar caso de uso exitosamente"""
        # Preparar datos
        request = ProcessStripeWebhookDTO(
            payload='{"id": "evt_test123", "type": "customer.created"}',
            signature="t=1640995200,v1=abc123"
        )
        
        event_data = {
            "id": "evt_test123",
            "type": "customer.created",
            "data": {
                "object": {
                    "id": "cus_test123"
                }
            }
        }
        
        mock_stripe_service.stripe_service.verify_webhook_signature.return_value = event_data
        
        processed_transaction = StripeTransaction(
            id="1",
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            status="processed",
            processed_at=datetime.now(),
            created_at=datetime.now()
        )
        
        mock_stripe_service.process_stripe_event.return_value = processed_transaction
        
        # Ejecutar
        result = await use_case.execute(request)
        
        # Verificar
        mock_stripe_service.stripe_service.verify_webhook_signature.assert_called_once_with(
            payload=request.payload.encode(),
            signature=request.signature
        )
        
        mock_stripe_service.process_stripe_event.assert_called_once_with(event_data)
        
        assert result.stripe_event_id == "evt_test123"
        assert result.event_type == StripeEventType.CUSTOMER_CREATED
        assert result.object_id == "cus_test123"
        assert result.status == "processed"
    
    @pytest.mark.asyncio
    async def test_execute_invalid_signature(self, use_case, mock_stripe_service):
        """Test ejecutar con firma inválida"""
        # Preparar datos
        request = ProcessStripeWebhookDTO(
            payload='{"id": "evt_test123", "type": "customer.created"}',
            signature="invalid_signature"
        )
        
        mock_stripe_service.stripe_service.verify_webhook_signature.side_effect = ValueError("Invalid signature")
        
        # Ejecutar y verificar excepción
        with pytest.raises(ValueError, match="Invalid signature"):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_execute_processing_error(self, use_case, mock_stripe_service):
        """Test ejecutar con error en procesamiento"""
        # Preparar datos
        request = ProcessStripeWebhookDTO(
            payload='{"id": "evt_test123", "type": "customer.created"}',
            signature="t=1640995200,v1=abc123"
        )
        
        event_data = {
            "id": "evt_test123",
            "type": "customer.created",
            "data": {
                "object": {
                    "id": "cus_test123"
                }
            }
        }
        
        mock_stripe_service.stripe_service.verify_webhook_signature.return_value = event_data
        mock_stripe_service.process_stripe_event.side_effect = Exception("Processing failed")
        
        # Ejecutar y verificar excepción
        with pytest.raises(Exception, match="Processing failed"):
            await use_case.execute(request)