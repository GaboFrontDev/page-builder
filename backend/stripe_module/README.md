# Stripe Module - Refactored

Módulo de integración con Stripe implementado siguiendo principios de Clean Architecture y **separación de responsabilidades**.

## 🎯 Principio de Separación de Responsabilidades

Este módulo se enfoca **exclusivamente** en operaciones de Stripe:
- ✅ Crear/cancelar suscripciones en Stripe
- ✅ Gestionar customers en Stripe
- ✅ Procesar webhooks de Stripe
- ✅ Sincronizar datos de Stripe con BD local
- ✅ Publicar eventos para comunicación entre módulos

**NO** maneja:
- ❌ Lógica de features premium de usuarios
- ❌ Actualización de estado de usuarios
- ❌ Lógica de negocio de la aplicación

## Estructura del Proyecto

```
stripe_module/
├── domain/                     # Capa de dominio
│   ├── entities/              # Entidades de Stripe
│   │   ├── __init__.py
│   │   └── subscription.py    # StripeCustomer, StripeSubscription, etc.
│   ├── repositories/          # Interfaces de repositorios
│   │   ├── __init__.py
│   │   ├── subscription_repository.py
│   │   └── stripe_service.py
│   ├── services/              # Servicios de dominio
│   │   ├── __init__.py
│   │   └── stripe_domain_service.py
│   └── events/                # Sistema de eventos
│       ├── __init__.py
│       ├── stripe_events.py
│       └── event_publisher.py
├── application/               # Capa de aplicación
│   ├── dto/                   # Data Transfer Objects
│   │   ├── __init__.py
│   │   └── stripe_dto.py
│   ├── use_cases/             # Casos de uso
│   │   ├── __init__.py
│   │   └── stripe_use_cases.py
│   └── __init__.py
├── infrastructure/            # Capa de infraestructura
│   ├── config/                # Configuración
│   │   ├── __init__.py
│   │   ├── stripe_config.py
│   │   └── .env.example
│   ├── models/                # Modelos de base de datos
│   │   └── subscription_models.py
│   ├── repositories/          # Implementaciones de repositorios
│   │   ├── __init__.py
│   │   └── sqlalchemy_subscription_repository.py
│   ├── stripe_client/         # Cliente de Stripe
│   │   ├── __init__.py
│   │   └── stripe_client.py
│   └── __init__.py
├── presentation/              # Capa de presentación
│   ├── __init__.py
│   └── stripe_api.py
├── examples/                  # Ejemplos de uso
│   └── user_subscription_handler.py
├── stripe_factory.py          # Factory para dependency injection
├── __init__.py
└── README.md
```

## 📝 Entidades Principales

### StripeCustomer
Representa un customer de Stripe con información básica:
- `stripe_customer_id`: ID único en Stripe
- `email`: Email del customer
- `name`: Nombre opcional
- `metadata`: Datos adicionales

### StripeSubscription
Representa una suscripción de Stripe:
- `stripe_subscription_id`: ID único en Stripe
- `stripe_customer_id`: ID del customer
- `stripe_price_id`: ID del precio
- `status`: Estado de la suscripción
- `current_period_start/end`: Periodo actual
- `metadata`: Datos adicionales

### StripeTransaction
Representa transacciones/eventos de Stripe:
- `stripe_event_id`: ID del evento
- `event_type`: Tipo de evento
- `object_id`: ID del objeto relacionado
- `amount`: Monto en centavos
- `status`: Estado de la transacción

## 🔄 Sistema de Eventos

El módulo publica eventos para comunicación entre módulos:

```python
# Eventos disponibles
StripeEventType.CUSTOMER_CREATED
StripeEventType.SUBSCRIPTION_CREATED
StripeEventType.SUBSCRIPTION_UPDATED
StripeEventType.SUBSCRIPTION_CANCELED
StripeEventType.PAYMENT_SUCCEEDED
StripeEventType.PAYMENT_FAILED
```

### Cómo Suscribirse a Eventos

```python
from stripe_module.domain.events import InMemoryEventPublisher, StripeEventType

# Crear publisher
publisher = InMemoryEventPublisher()

# Crear handler personalizado
class UserHandler(EventSubscriber):
    async def handle(self, event: StripeEvent):
        if event.event_type == StripeEventType.SUBSCRIPTION_CREATED:
            # Activar features premium en módulo de usuario
            await self.activate_user_premium_features(event.data.customer_id)

# Suscribir handler
handler = UserHandler()
publisher.subscribe(StripeEventType.SUBSCRIPTION_CREATED, handler)
```

## 🛠️ Casos de Uso Principales

### 1. Crear Customer en Stripe
```python
from stripe_module.application import CreateStripeCustomerDTO

dto = CreateStripeCustomerDTO(
    email="user@example.com",
    name="John Doe"
)

result = await create_customer_use_case.execute(dto)
```

### 2. Crear Suscripción
```python
from stripe_module.application import CreateStripeSubscriptionDTO

dto = CreateStripeSubscriptionDTO(
    customer_id="cus_stripe_id",
    price_id="price_stripe_id",
    payment_method_id="pm_stripe_id"
)

result = await create_subscription_use_case.execute(dto)
```

### 3. Procesar Webhook
```python
from stripe_module.application import ProcessStripeWebhookDTO

dto = ProcessStripeWebhookDTO(
    payload=request_body,
    signature=stripe_signature
)

result = await process_webhook_use_case.execute(dto)
```

## 🌐 Endpoints API

### Customers
- `POST /stripe/customers` - Crear customer
- `GET /stripe/customers/{customer_id}/subscriptions` - Obtener suscripciones
- `GET /stripe/customers/{customer_id}/payment-methods` - Obtener métodos de pago

### Suscripciones
- `POST /stripe/subscriptions` - Crear suscripción
- `DELETE /stripe/subscriptions/{subscription_id}` - Cancelar suscripción

### Métodos de Pago
- `POST /stripe/payment-methods/setup` - Configurar método de pago

### Sincronización
- `POST /stripe/sync/{object_type}/{object_id}` - Sincronizar objeto desde Stripe

### Precios
- `GET /stripe/prices` - Obtener precios
- `POST /stripe/prices/sync` - Sincronizar precios

### Webhooks
- `POST /stripe/webhooks` - Procesar webhooks

### Utilidades
- `GET /stripe/health` - Health check del módulo

## 🔧 Configuración

### Variables de Entorno
```env
# Claves de Stripe
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Price IDs
STRIPE_PRICE_BASIC_MONTHLY=price_basic_id
STRIPE_PRICE_PREMIUM_MONTHLY=price_premium_id
STRIPE_PRICE_ENTERPRISE_MONTHLY=price_enterprise_id

# Configuración
STRIPE_API_VERSION=2023-10-16
STRIPE_SUCCESS_URL=http://localhost:3000/success
STRIPE_CANCEL_URL=http://localhost:3000/cancel
```

## 📖 Ejemplo de Integración

### 1. Configurar el Módulo
```python
from fastapi import FastAPI
from stripe_module import stripe_router

app = FastAPI()
app.include_router(stripe_router)
```

### 2. Configurar Event Handlers
```python
from stripe_module.domain.events import InMemoryEventPublisher, StripeEventPublisher

# Crear publisher
publisher = InMemoryEventPublisher()
stripe_publisher = StripeEventPublisher(publisher)

# Crear handler para actualizar usuarios
class UserSubscriptionHandler(EventSubscriber):
    async def handle(self, event: StripeEvent):
        if event.event_type == StripeEventType.SUBSCRIPTION_CREATED:
            await user_service.activate_premium_features(event.data.customer_id)
        elif event.event_type == StripeEventType.SUBSCRIPTION_CANCELED:
            await user_service.deactivate_premium_features(event.data.customer_id)

# Suscribir handler
handler = UserSubscriptionHandler()
publisher.subscribe(StripeEventType.SUBSCRIPTION_CREATED, handler)
publisher.subscribe(StripeEventType.SUBSCRIPTION_CANCELED, handler)
```

## 🧪 Testing

### Mocking del Servicio de Stripe
```python
from unittest.mock import Mock
from stripe_module.domain.services import StripeDomainService

# Mock del StripeService
mock_stripe_service = Mock()
mock_stripe_service.create_customer.return_value = {"id": "cus_test"}

# Crear servicio de dominio con mocks
domain_service = StripeDomainService(
    stripe_service=mock_stripe_service,
    customer_repo=mock_customer_repo,
    # ... otros repos
)
```

### Testing de Casos de Uso
```python
from stripe_module.application import CreateStripeCustomerUseCase

# Crear caso de uso con mocks
use_case = CreateStripeCustomerUseCase(
    stripe_service=mock_domain_service,
    event_publisher=mock_event_publisher
)

# Ejecutar test
result = await use_case.execute(CreateStripeCustomerDTO(
    email="test@example.com"
))

assert result.email == "test@example.com"
```

## 🔒 Seguridad

- ✅ Verificación de firmas de webhook
- ✅ Validación de datos de entrada con Pydantic
- ✅ Manejo seguro de claves API
- ✅ Separación de entornos development/production
- ✅ Logs de transacciones para auditoría

## 📈 Ventajas de Esta Arquitectura

1. **Separación Clara**: Stripe solo maneja operaciones de Stripe
2. **Comunicación por Eventos**: Módulos desacoplados
3. **Fácil Testing**: Cada componente se puede testear por separado
4. **Mantenibilidad**: Cambios en Stripe no afectan otros módulos
5. **Extensibilidad**: Fácil agregar nuevos handlers de eventos
6. **Trazabilidad**: Registro completo de transacciones

## 🚀 Próximos Pasos

1. Implementar repositorios concretos con SQLAlchemy
2. Crear migraciones de base de datos
3. Configurar webhooks en Stripe Dashboard
4. Implementar handlers de eventos en módulos de usuario
5. Configurar monitoreo y logging

## 📚 Recursos Adicionales

- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Clean Architecture Principles](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)