from typing import Optional
from sqlalchemy.orm import Session

from .domain.repositories import (
    StripeService,
    StripeCustomerRepository,
    StripeSubscriptionRepository,
    StripePaymentMethodRepository,
    StripeTransactionRepository,
    StripePriceRepository
)
from .domain.services import StripeDomainService
from .domain.events import InMemoryEventPublisher, StripeEventPublisher
from .application import (
    CreateStripeCustomerUseCase,
    CreateStripeSubscriptionUseCase,
    CancelStripeSubscriptionUseCase,
    SetupStripePaymentMethodUseCase,
    GetStripeCustomerSubscriptionsUseCase,
    GetStripeCustomerPaymentMethodsUseCase,
    SyncStripeObjectUseCase,
    ProcessStripeWebhookUseCase,
    GetStripePricesUseCase,
    SyncStripePricesUseCase
)
from .infrastructure import (
    StripeClient,
    SQLAlchemyStripeCustomerRepository,
    SQLAlchemyStripeSubscriptionRepository,
    SQLAlchemyStripePaymentMethodRepository,
    SQLAlchemyStripeTransactionRepository,
    SQLAlchemyStripePriceRepository
)


class StripeModuleFactory:
    """Factory para crear instancias de los componentes del módulo Stripe refactorizado"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._stripe_client: Optional[StripeClient] = None
        self._customer_repo: Optional[StripeCustomerRepository] = None
        self._subscription_repo: Optional[StripeSubscriptionRepository] = None
        self._payment_method_repo: Optional[StripePaymentMethodRepository] = None
        self._transaction_repo: Optional[StripeTransactionRepository] = None
        self._price_repo: Optional[StripePriceRepository] = None
        self._stripe_domain_service: Optional[StripeDomainService] = None
        self._event_publisher: Optional[InMemoryEventPublisher] = None
        self._stripe_event_publisher: Optional[StripeEventPublisher] = None
    
    def get_stripe_client(self) -> StripeClient:
        """Obtener cliente de Stripe (singleton)"""
        if self._stripe_client is None:
            self._stripe_client = StripeClient()
        return self._stripe_client
    
    def get_customer_repository(self) -> StripeCustomerRepository:
        """Obtener repositorio de customers de Stripe"""
        if self._customer_repo is None:
            self._customer_repo = SQLAlchemyStripeCustomerRepository(self.db_session)
        return self._customer_repo
    
    def get_subscription_repository(self) -> StripeSubscriptionRepository:
        """Obtener repositorio de suscripciones de Stripe"""
        if self._subscription_repo is None:
            self._subscription_repo = SQLAlchemyStripeSubscriptionRepository(self.db_session)
        return self._subscription_repo
    
    def get_payment_method_repository(self) -> StripePaymentMethodRepository:
        """Obtener repositorio de métodos de pago de Stripe"""
        if self._payment_method_repo is None:
            self._payment_method_repo = SQLAlchemyStripePaymentMethodRepository(self.db_session)
        return self._payment_method_repo
    
    def get_transaction_repository(self) -> StripeTransactionRepository:
        """Obtener repositorio de transacciones de Stripe"""
        if self._transaction_repo is None:
            self._transaction_repo = SQLAlchemyStripeTransactionRepository(self.db_session)
        return self._transaction_repo
    
    def get_price_repository(self) -> StripePriceRepository:
        """Obtener repositorio de precios de Stripe"""
        if self._price_repo is None:
            self._price_repo = SQLAlchemyStripePriceRepository(self.db_session)
        return self._price_repo
    
    def get_event_publisher(self) -> InMemoryEventPublisher:
        """Obtener event publisher"""
        if self._event_publisher is None:
            self._event_publisher = InMemoryEventPublisher()
        return self._event_publisher
    
    def get_stripe_event_publisher(self) -> StripeEventPublisher:
        """Obtener Stripe event publisher"""
        if self._stripe_event_publisher is None:
            self._stripe_event_publisher = StripeEventPublisher(self.get_event_publisher())
        return self._stripe_event_publisher
    
    def get_stripe_domain_service(self) -> StripeDomainService:
        """Obtener servicio de dominio de Stripe"""
        if self._stripe_domain_service is None:
            self._stripe_domain_service = StripeDomainService(
                stripe_service=self.get_stripe_client(),
                customer_repo=self.get_customer_repository(),
                subscription_repo=self.get_subscription_repository(),
                payment_method_repo=self.get_payment_method_repository(),
                transaction_repo=self.get_transaction_repository(),
                price_repo=self.get_price_repository()
            )
        return self._stripe_domain_service
    
    # Use Cases
    def get_create_customer_use_case(self) -> CreateStripeCustomerUseCase:
        """Obtener caso de uso para crear customer"""
        return CreateStripeCustomerUseCase(
            stripe_service=self.get_stripe_domain_service(),
            event_publisher=self.get_stripe_event_publisher()
        )
    
    def get_create_subscription_use_case(self) -> CreateStripeSubscriptionUseCase:
        """Obtener caso de uso para crear suscripción"""
        return CreateStripeSubscriptionUseCase(
            stripe_service=self.get_stripe_domain_service(),
            event_publisher=self.get_stripe_event_publisher()
        )
    
    def get_cancel_subscription_use_case(self) -> CancelStripeSubscriptionUseCase:
        """Obtener caso de uso para cancelar suscripción"""
        return CancelStripeSubscriptionUseCase(
            stripe_service=self.get_stripe_domain_service(),
            event_publisher=self.get_stripe_event_publisher()
        )
    
    def get_setup_payment_method_use_case(self) -> SetupStripePaymentMethodUseCase:
        """Obtener caso de uso para configurar método de pago"""
        return SetupStripePaymentMethodUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_customer_subscriptions_use_case(self) -> GetStripeCustomerSubscriptionsUseCase:
        """Obtener caso de uso para obtener suscripciones de customer"""
        return GetStripeCustomerSubscriptionsUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_customer_payment_methods_use_case(self) -> GetStripeCustomerPaymentMethodsUseCase:
        """Obtener caso de uso para obtener métodos de pago de customer"""
        return GetStripeCustomerPaymentMethodsUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_sync_object_use_case(self) -> SyncStripeObjectUseCase:
        """Obtener caso de uso para sincronizar objeto"""
        return SyncStripeObjectUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_process_webhook_use_case(self) -> ProcessStripeWebhookUseCase:
        """Obtener caso de uso para procesar webhook"""
        return ProcessStripeWebhookUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_prices_use_case(self) -> GetStripePricesUseCase:
        """Obtener caso de uso para obtener precios"""
        return GetStripePricesUseCase(
            stripe_service=self.get_stripe_domain_service()
        )
    
    def get_sync_prices_use_case(self) -> SyncStripePricesUseCase:
        """Obtener caso de uso para sincronizar precios"""
        return SyncStripePricesUseCase(
            stripe_service=self.get_stripe_domain_service()
        )


# Instancia global del factory (se inicializará cuando se tenga la sesión de BD)
_stripe_factory: Optional[StripeModuleFactory] = None


def get_stripe_factory(db_session: Session) -> StripeModuleFactory:
    """Obtener factory de Stripe"""
    global _stripe_factory
    if _stripe_factory is None:
        _stripe_factory = StripeModuleFactory(db_session)
    return _stripe_factory


def reset_stripe_factory():
    """Resetear factory (útil para testing)"""
    global _stripe_factory
    _stripe_factory = None


# Funciones de dependencia para FastAPI
def get_stripe_client_dependency(db: Session):
    """Dependency para obtener cliente de Stripe"""
    factory = get_stripe_factory(db)
    return factory.get_stripe_client()


def get_create_customer_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de crear customer"""
    factory = get_stripe_factory(db)
    return factory.get_create_customer_use_case()


def get_create_subscription_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de crear suscripción"""
    factory = get_stripe_factory(db)
    return factory.get_create_subscription_use_case()


def get_cancel_subscription_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de cancelar suscripción"""
    factory = get_stripe_factory(db)
    return factory.get_cancel_subscription_use_case()


def get_setup_payment_method_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de configurar método de pago"""
    factory = get_stripe_factory(db)
    return factory.get_setup_payment_method_use_case()


def get_customer_subscriptions_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de obtener suscripciones de customer"""
    factory = get_stripe_factory(db)
    return factory.get_customer_subscriptions_use_case()


def get_customer_payment_methods_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de obtener métodos de pago de customer"""
    factory = get_stripe_factory(db)
    return factory.get_customer_payment_methods_use_case()


def get_sync_object_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de sincronizar objeto"""
    factory = get_stripe_factory(db)
    return factory.get_sync_object_use_case()


def get_process_webhook_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de procesar webhook"""
    factory = get_stripe_factory(db)
    return factory.get_process_webhook_use_case()


def get_prices_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de obtener precios"""
    factory = get_stripe_factory(db)
    return factory.get_prices_use_case()


def get_sync_prices_use_case_dependency(db: Session):
    """Dependency para obtener caso de uso de sincronizar precios"""
    factory = get_stripe_factory(db)
    return factory.get_sync_prices_use_case()