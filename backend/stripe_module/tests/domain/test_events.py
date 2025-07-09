import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from ...domain.events import (
    StripeEvent,
    StripeEventData,
    StripeEventType,
    StripeEventStatus,
    EventSubscriber,
    InMemoryEventPublisher,
    StripeEventPublisher
)


class TestStripeEventData:
    """Tests para StripeEventData"""
    
    def test_create_event_data_minimal(self):
        """Test crear event data con datos mínimos"""
        occurred_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        assert event_data.stripe_event_id == "evt_test123"
        assert event_data.event_type == StripeEventType.CUSTOMER_CREATED
        assert event_data.object_id == "cus_test123"
        assert event_data.occurred_at == occurred_at
        assert event_data.customer_id is None
        assert event_data.subscription_id is None
        assert event_data.amount is None
        assert event_data.currency is None
        assert event_data.status is None
        assert event_data.metadata == {}
    
    def test_create_event_data_full(self):
        """Test crear event data con todos los datos"""
        occurred_at = datetime.now()
        metadata = {"user_id": "123"}
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.PAYMENT_SUCCEEDED,
            object_id="in_test123",
            customer_id="cus_test123",
            subscription_id="sub_test123",
            amount=2000,
            currency="usd",
            status="succeeded",
            metadata=metadata,
            occurred_at=occurred_at
        )
        
        assert event_data.customer_id == "cus_test123"
        assert event_data.subscription_id == "sub_test123"
        assert event_data.amount == 2000
        assert event_data.currency == "usd"
        assert event_data.status == "succeeded"
        assert event_data.metadata == metadata


class TestStripeEvent:
    """Tests para StripeEvent"""
    
    def test_create_event_minimal(self):
        """Test crear evento con datos mínimos"""
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        assert event.event_type == StripeEventType.CUSTOMER_CREATED
        assert event.data == event_data
        assert event.status == StripeEventStatus.PENDING
        assert event.retry_count == 0
        assert event.max_retries == 3
        assert event.error_message is None
        assert event.created_at == created_at
        assert event.processed_at is None
    
    def test_mark_as_processing(self):
        """Test marcar evento como en procesamiento"""
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        event.mark_as_processing()
        assert event.status == StripeEventStatus.PROCESSING
    
    def test_mark_as_completed(self):
        """Test marcar evento como completado"""
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        event.mark_as_completed()
        assert event.status == StripeEventStatus.COMPLETED
        assert event.processed_at is not None
    
    def test_mark_as_failed(self):
        """Test marcar evento como fallido"""
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        error_message = "Processing failed"
        event.mark_as_failed(error_message)
        
        assert event.status == StripeEventStatus.FAILED
        assert event.error_message == error_message
        assert event.retry_count == 1
    
    def test_can_retry(self):
        """Test verificar si evento puede ser reintentado"""
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        # Inicialmente puede ser reintentado
        assert event.can_retry() is False  # Porque no ha fallado
        
        # Después de fallar, puede ser reintentado
        event.mark_as_failed("Error 1")
        assert event.can_retry() is True
        
        # Después de máximo reintentos, no puede ser reintentado
        event.mark_as_failed("Error 2")
        event.mark_as_failed("Error 3")
        assert event.can_retry() is False
        assert event.retry_count == 3


class MockEventSubscriber(EventSubscriber):
    """Mock subscriber para tests"""
    
    def __init__(self):
        self.handled_events = []
        self.should_fail = False
    
    async def handle(self, event: StripeEvent) -> None:
        if self.should_fail:
            raise Exception("Handler failed")
        self.handled_events.append(event)


class TestInMemoryEventPublisher:
    """Tests para InMemoryEventPublisher"""
    
    def test_subscribe_and_publish(self):
        """Test suscribir y publicar eventos"""
        publisher = InMemoryEventPublisher()
        subscriber = MockEventSubscriber()
        
        # Suscribir
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber)
        
        # Verificar suscripción
        assert StripeEventType.CUSTOMER_CREATED in publisher.subscribers
        assert subscriber in publisher.subscribers[StripeEventType.CUSTOMER_CREATED]
    
    @pytest.mark.asyncio
    async def test_publish_event(self):
        """Test publicar evento"""
        publisher = InMemoryEventPublisher()
        subscriber = MockEventSubscriber()
        
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber)
        
        # Crear evento
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        # Publicar evento
        await publisher.publish(event)
        
        # Verificar que el subscriber recibió el evento
        assert len(subscriber.handled_events) == 1
        assert subscriber.handled_events[0] == event
    
    @pytest.mark.asyncio
    async def test_publish_event_to_multiple_subscribers(self):
        """Test publicar evento a múltiples subscribers"""
        publisher = InMemoryEventPublisher()
        subscriber1 = MockEventSubscriber()
        subscriber2 = MockEventSubscriber()
        
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber1)
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber2)
        
        # Crear evento
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        # Publicar evento
        await publisher.publish(event)
        
        # Verificar que ambos subscribers recibieron el evento
        assert len(subscriber1.handled_events) == 1
        assert len(subscriber2.handled_events) == 1
        assert subscriber1.handled_events[0] == event
        assert subscriber2.handled_events[0] == event
    
    @pytest.mark.asyncio
    async def test_publish_event_with_failing_subscriber(self):
        """Test publicar evento con subscriber que falla"""
        publisher = InMemoryEventPublisher()
        subscriber1 = MockEventSubscriber()
        subscriber2 = MockEventSubscriber()
        
        # Hacer que el primer subscriber falle
        subscriber1.should_fail = True
        
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber1)
        publisher.subscribe(StripeEventType.CUSTOMER_CREATED, subscriber2)
        
        # Crear evento
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        # Publicar evento (no debería lanzar excepción)
        await publisher.publish(event)
        
        # Verificar que el segundo subscriber sí recibió el evento
        assert len(subscriber1.handled_events) == 0
        assert len(subscriber2.handled_events) == 1
        assert subscriber2.handled_events[0] == event
    
    @pytest.mark.asyncio
    async def test_publish_event_no_subscribers(self):
        """Test publicar evento sin subscribers"""
        publisher = InMemoryEventPublisher()
        
        # Crear evento
        occurred_at = datetime.now()
        created_at = datetime.now()
        
        event_data = StripeEventData(
            stripe_event_id="evt_test123",
            event_type=StripeEventType.CUSTOMER_CREATED,
            object_id="cus_test123",
            occurred_at=occurred_at
        )
        
        event = StripeEvent(
            event_type=StripeEventType.CUSTOMER_CREATED,
            data=event_data,
            created_at=created_at
        )
        
        # Publicar evento (no debería lanzar excepción)
        await publisher.publish(event)


class TestStripeEventPublisher:
    """Tests para StripeEventPublisher"""
    
    @pytest.mark.asyncio
    async def test_publish_customer_created(self):
        """Test publicar evento de customer creado"""
        mock_publisher = Mock()
        mock_publisher.publish = AsyncMock()
        
        stripe_publisher = StripeEventPublisher(mock_publisher)
        
        await stripe_publisher.publish_customer_created(
            customer_id="cus_test123",
            email="test@example.com",
            metadata={"user_id": "123"}
        )
        
        # Verificar que se llamó al publisher
        mock_publisher.publish.assert_called_once()
        
        # Verificar el evento publicado
        call_args = mock_publisher.publish.call_args[0]
        event = call_args[0]
        
        assert event.event_type == StripeEventType.CUSTOMER_CREATED
        assert event.data.object_id == "cus_test123"
        assert event.data.customer_id == "cus_test123"
        assert event.data.metadata == {"user_id": "123"}
    
    @pytest.mark.asyncio
    async def test_publish_subscription_created(self):
        """Test publicar evento de suscripción creada"""
        mock_publisher = Mock()
        mock_publisher.publish = AsyncMock()
        
        stripe_publisher = StripeEventPublisher(mock_publisher)
        
        await stripe_publisher.publish_subscription_created(
            subscription_id="sub_test123",
            customer_id="cus_test123",
            price_id="price_test123",
            metadata={"plan": "basic"}
        )
        
        # Verificar que se llamó al publisher
        mock_publisher.publish.assert_called_once()
        
        # Verificar el evento publicado
        call_args = mock_publisher.publish.call_args[0]
        event = call_args[0]
        
        assert event.event_type == StripeEventType.SUBSCRIPTION_CREATED
        assert event.data.object_id == "sub_test123"
        assert event.data.customer_id == "cus_test123"
        assert event.data.subscription_id == "sub_test123"
        assert event.data.metadata == {"plan": "basic"}
    
    @pytest.mark.asyncio
    async def test_publish_payment_succeeded(self):
        """Test publicar evento de pago exitoso"""
        mock_publisher = Mock()
        mock_publisher.publish = AsyncMock()
        
        stripe_publisher = StripeEventPublisher(mock_publisher)
        
        await stripe_publisher.publish_payment_succeeded(
            customer_id="cus_test123",
            subscription_id="sub_test123",
            amount=2000,
            currency="usd",
            metadata={"invoice_id": "in_test123"}
        )
        
        # Verificar que se llamó al publisher
        mock_publisher.publish.assert_called_once()
        
        # Verificar el evento publicado
        call_args = mock_publisher.publish.call_args[0]
        event = call_args[0]
        
        assert event.event_type == StripeEventType.PAYMENT_SUCCEEDED
        assert event.data.customer_id == "cus_test123"
        assert event.data.subscription_id == "sub_test123"
        assert event.data.amount == 2000
        assert event.data.currency == "usd"
        assert event.data.metadata == {"invoice_id": "in_test123"}
    
    @pytest.mark.asyncio
    async def test_publish_payment_failed(self):
        """Test publicar evento de pago fallido"""
        mock_publisher = Mock()
        mock_publisher.publish = AsyncMock()
        
        stripe_publisher = StripeEventPublisher(mock_publisher)
        
        await stripe_publisher.publish_payment_failed(
            customer_id="cus_test123",
            subscription_id="sub_test123",
            amount=2000,
            currency="usd",
            error_message="Card declined",
            metadata={"invoice_id": "in_test123"}
        )
        
        # Verificar que se llamó al publisher
        mock_publisher.publish.assert_called_once()
        
        # Verificar el evento publicado
        call_args = mock_publisher.publish.call_args[0]
        event = call_args[0]
        
        assert event.event_type == StripeEventType.PAYMENT_FAILED
        assert event.data.customer_id == "cus_test123"
        assert event.data.subscription_id == "sub_test123"
        assert event.data.amount == 2000
        assert event.data.currency == "usd"
        assert event.data.status == "failed"
        assert event.data.metadata == {"invoice_id": "in_test123"}