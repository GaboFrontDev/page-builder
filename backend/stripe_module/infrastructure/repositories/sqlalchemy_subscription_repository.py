from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from ...domain.entities import (
    StripeCustomer,
    StripeSubscription,
    StripePaymentMethod,
    StripeTransaction,
    StripePrice
)
from ...domain.repositories import (
    StripeCustomerRepository,
    StripeSubscriptionRepository,
    StripePaymentMethodRepository,
    StripeTransactionRepository,
    StripePriceRepository
)
from ..models.subscription_models import (
    StripeCustomerModel,
    StripeSubscriptionModel,
    StripePaymentMethodModel,
    StripeTransactionModel,
    StripePriceModel
)


class SQLAlchemyStripeCustomerRepository(StripeCustomerRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create_customer(self, customer: StripeCustomer) -> StripeCustomer:
        db_customer = StripeCustomerModel(
            stripe_customer_id=customer.stripe_customer_id,
            email=customer.email,
            name=customer.name,
            phone=customer.phone,
            metadata=customer.metadata
        )
        
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        
        return self._to_entity(db_customer)
    
    async def get_customer_by_stripe_id(self, stripe_customer_id: str) -> Optional[StripeCustomer]:
        stmt = select(StripeCustomerModel).where(StripeCustomerModel.stripe_customer_id == stripe_customer_id)
        result = self.db.execute(stmt)
        db_customer = result.scalar_one_or_none()
        
        if db_customer:
            return self._to_entity(db_customer)
        return None
    
    async def get_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        stmt = select(StripeCustomerModel).where(StripeCustomerModel.email == email)
        result = self.db.execute(stmt)
        db_customer = result.scalar_one_or_none()
        
        if db_customer:
            return self._to_entity(db_customer)
        return None
    
    async def update_customer(self, customer: StripeCustomer) -> StripeCustomer:
        stmt = select(StripeCustomerModel).where(StripeCustomerModel.stripe_customer_id == customer.stripe_customer_id)
        result = self.db.execute(stmt)
        db_customer = result.scalar_one_or_none()
        
        if db_customer:
            db_customer.email = customer.email
            db_customer.name = customer.name
            db_customer.phone = customer.phone
            db_customer.metadata = customer.metadata
            
            self.db.commit()
            self.db.refresh(db_customer)
            return self._to_entity(db_customer)
        
        raise ValueError("Customer not found")
    
    async def delete_customer(self, stripe_customer_id: str) -> bool:
        stmt = select(StripeCustomerModel).where(StripeCustomerModel.stripe_customer_id == stripe_customer_id)
        result = self.db.execute(stmt)
        db_customer = result.scalar_one_or_none()
        
        if db_customer:
            self.db.delete(db_customer)
            self.db.commit()
            return True
        
        return False
    
    def _to_entity(self, db_customer: StripeCustomerModel) -> StripeCustomer:
        return StripeCustomer(
            id=str(db_customer.id),
            stripe_customer_id=db_customer.stripe_customer_id,
            email=db_customer.email,
            name=db_customer.name,
            phone=db_customer.phone,
            metadata=db_customer.metadata,
            created_at=db_customer.created_at
        )


class SQLAlchemyStripeSubscriptionRepository(StripeSubscriptionRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create_subscription(self, subscription: StripeSubscription) -> StripeSubscription:
        db_subscription = StripeSubscriptionModel(
            stripe_subscription_id=subscription.stripe_subscription_id,
            stripe_customer_id=subscription.stripe_customer_id,
            stripe_price_id=subscription.stripe_price_id,
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            canceled_at=subscription.canceled_at,
            trial_start=subscription.trial_start,
            trial_end=subscription.trial_end,
            metadata=subscription.metadata
        )
        
        self.db.add(db_subscription)
        self.db.commit()
        self.db.refresh(db_subscription)
        
        return self._to_entity(db_subscription)
    
    async def get_subscription_by_stripe_id(self, stripe_subscription_id: str) -> Optional[StripeSubscription]:
        stmt = select(StripeSubscriptionModel).where(StripeSubscriptionModel.stripe_subscription_id == stripe_subscription_id)
        result = self.db.execute(stmt)
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            return self._to_entity(db_subscription)
        return None
    
    async def get_subscriptions_by_customer_id(self, stripe_customer_id: str) -> List[StripeSubscription]:
        stmt = select(StripeSubscriptionModel).where(StripeSubscriptionModel.stripe_customer_id == stripe_customer_id)
        result = self.db.execute(stmt)
        db_subscriptions = result.scalars().all()
        
        return [self._to_entity(sub) for sub in db_subscriptions]
    
    async def update_subscription(self, subscription: StripeSubscription) -> StripeSubscription:
        stmt = select(StripeSubscriptionModel).where(StripeSubscriptionModel.stripe_subscription_id == subscription.stripe_subscription_id)
        result = self.db.execute(stmt)
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            db_subscription.status = subscription.status
            db_subscription.current_period_start = subscription.current_period_start
            db_subscription.current_period_end = subscription.current_period_end
            db_subscription.cancel_at_period_end = subscription.cancel_at_period_end
            db_subscription.canceled_at = subscription.canceled_at
            db_subscription.trial_start = subscription.trial_start
            db_subscription.trial_end = subscription.trial_end
            db_subscription.metadata = subscription.metadata
            
            self.db.commit()
            self.db.refresh(db_subscription)
            return self._to_entity(db_subscription)
        
        raise ValueError("Subscription not found")
    
    async def delete_subscription(self, stripe_subscription_id: str) -> bool:
        stmt = select(StripeSubscriptionModel).where(StripeSubscriptionModel.stripe_subscription_id == stripe_subscription_id)
        result = self.db.execute(stmt)
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            self.db.delete(db_subscription)
            self.db.commit()
            return True
        
        return False
    
    def _to_entity(self, db_subscription: StripeSubscriptionModel) -> StripeSubscription:
        return StripeSubscription(
            id=str(db_subscription.id),
            stripe_subscription_id=db_subscription.stripe_subscription_id,
            stripe_customer_id=db_subscription.stripe_customer_id,
            stripe_price_id=db_subscription.stripe_price_id,
            status=db_subscription.status,
            current_period_start=db_subscription.current_period_start,
            current_period_end=db_subscription.current_period_end,
            cancel_at_period_end=db_subscription.cancel_at_period_end,
            canceled_at=db_subscription.canceled_at,
            trial_start=db_subscription.trial_start,
            trial_end=db_subscription.trial_end,
            metadata=db_subscription.metadata,
            created_at=db_subscription.created_at,
            updated_at=db_subscription.updated_at
        )


class SQLAlchemyStripePaymentMethodRepository(StripePaymentMethodRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create_payment_method(self, payment_method: StripePaymentMethod) -> StripePaymentMethod:
        db_payment_method = StripePaymentMethodModel(
            stripe_payment_method_id=payment_method.stripe_payment_method_id,
            stripe_customer_id=payment_method.stripe_customer_id,
            type=payment_method.type,
            card_last4=payment_method.card_last4,
            card_brand=payment_method.card_brand,
            card_exp_month=payment_method.card_exp_month,
            card_exp_year=payment_method.card_exp_year,
            is_default=payment_method.is_default
        )
        
        self.db.add(db_payment_method)
        self.db.commit()
        self.db.refresh(db_payment_method)
        
        return self._to_entity(db_payment_method)
    
    async def get_payment_methods_by_customer_id(self, stripe_customer_id: str) -> List[StripePaymentMethod]:
        stmt = select(StripePaymentMethodModel).where(StripePaymentMethodModel.stripe_customer_id == stripe_customer_id)
        result = self.db.execute(stmt)
        db_payment_methods = result.scalars().all()
        
        return [self._to_entity(pm) for pm in db_payment_methods]
    
    async def get_payment_method_by_stripe_id(self, stripe_payment_method_id: str) -> Optional[StripePaymentMethod]:
        stmt = select(StripePaymentMethodModel).where(StripePaymentMethodModel.stripe_payment_method_id == stripe_payment_method_id)
        result = self.db.execute(stmt)
        db_payment_method = result.scalar_one_or_none()
        
        if db_payment_method:
            return self._to_entity(db_payment_method)
        return None
    
    async def get_default_payment_method(self, stripe_customer_id: str) -> Optional[StripePaymentMethod]:
        stmt = select(StripePaymentMethodModel).where(
            StripePaymentMethodModel.stripe_customer_id == stripe_customer_id,
            StripePaymentMethodModel.is_default == True
        )
        result = self.db.execute(stmt)
        db_payment_method = result.scalar_one_or_none()
        
        if db_payment_method:
            return self._to_entity(db_payment_method)
        return None
    
    async def update_payment_method(self, payment_method: StripePaymentMethod) -> StripePaymentMethod:
        stmt = select(StripePaymentMethodModel).where(
            StripePaymentMethodModel.stripe_payment_method_id == payment_method.stripe_payment_method_id
        )
        result = self.db.execute(stmt)
        db_payment_method = result.scalar_one_or_none()
        
        if db_payment_method:
            db_payment_method.type = payment_method.type
            db_payment_method.card_last4 = payment_method.card_last4
            db_payment_method.card_brand = payment_method.card_brand
            db_payment_method.card_exp_month = payment_method.card_exp_month
            db_payment_method.card_exp_year = payment_method.card_exp_year
            db_payment_method.is_default = payment_method.is_default
            
            self.db.commit()
            self.db.refresh(db_payment_method)
            return self._to_entity(db_payment_method)
        
        raise ValueError("Payment method not found")
    
    async def delete_payment_method(self, stripe_payment_method_id: str) -> bool:
        stmt = select(StripePaymentMethodModel).where(
            StripePaymentMethodModel.stripe_payment_method_id == stripe_payment_method_id
        )
        result = self.db.execute(stmt)
        db_payment_method = result.scalar_one_or_none()
        
        if db_payment_method:
            self.db.delete(db_payment_method)
            self.db.commit()
            return True
        
        return False
    
    def _to_entity(self, db_payment_method: StripePaymentMethodModel) -> StripePaymentMethod:
        return StripePaymentMethod(
            id=str(db_payment_method.id),
            stripe_payment_method_id=db_payment_method.stripe_payment_method_id,
            stripe_customer_id=db_payment_method.stripe_customer_id,
            type=db_payment_method.type,
            card_last4=db_payment_method.card_last4,
            card_brand=db_payment_method.card_brand,
            card_exp_month=db_payment_method.card_exp_month,
            card_exp_year=db_payment_method.card_exp_year,
            is_default=db_payment_method.is_default,
            created_at=db_payment_method.created_at
        )


class SQLAlchemyStripeTransactionRepository(StripeTransactionRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create_transaction(self, transaction: StripeTransaction) -> StripeTransaction:
        db_transaction = StripeTransactionModel(
            stripe_event_id=transaction.stripe_event_id,
            event_type=transaction.event_type,
            object_id=transaction.object_id,
            amount=transaction.amount,
            currency=transaction.currency,
            status=transaction.status,
            metadata=transaction.metadata,
            processed_at=transaction.processed_at
        )
        
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        
        return self._to_entity(db_transaction)
    
    async def get_transaction_by_stripe_event_id(self, stripe_event_id: str) -> Optional[StripeTransaction]:
        stmt = select(StripeTransactionModel).where(StripeTransactionModel.stripe_event_id == stripe_event_id)
        result = self.db.execute(stmt)
        db_transaction = result.scalar_one_or_none()
        
        if db_transaction:
            return self._to_entity(db_transaction)
        return None
    
    async def get_transactions_by_object_id(self, object_id: str) -> List[StripeTransaction]:
        stmt = select(StripeTransactionModel).where(StripeTransactionModel.object_id == object_id)
        result = self.db.execute(stmt)
        db_transactions = result.scalars().all()
        
        return [self._to_entity(tx) for tx in db_transactions]
    
    async def update_transaction(self, transaction: StripeTransaction) -> StripeTransaction:
        stmt = select(StripeTransactionModel).where(StripeTransactionModel.stripe_event_id == transaction.stripe_event_id)
        result = self.db.execute(stmt)
        db_transaction = result.scalar_one_or_none()
        
        if db_transaction:
            db_transaction.status = transaction.status
            db_transaction.metadata = transaction.metadata
            db_transaction.processed_at = transaction.processed_at
            
            self.db.commit()
            self.db.refresh(db_transaction)
            return self._to_entity(db_transaction)
        
        raise ValueError("Transaction not found")
    
    def _to_entity(self, db_transaction: StripeTransactionModel) -> StripeTransaction:
        return StripeTransaction(
            id=str(db_transaction.id),
            stripe_event_id=db_transaction.stripe_event_id,
            event_type=db_transaction.event_type,
            object_id=db_transaction.object_id,
            amount=db_transaction.amount,
            currency=db_transaction.currency,
            status=db_transaction.status,
            metadata=db_transaction.metadata,
            processed_at=db_transaction.processed_at,
            created_at=db_transaction.created_at
        )


class SQLAlchemyStripePriceRepository(StripePriceRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create_price(self, price: StripePrice) -> StripePrice:
        db_price = StripePriceModel(
            stripe_price_id=price.stripe_price_id,
            stripe_product_id=price.stripe_product_id,
            amount=price.amount,
            currency=price.currency,
            interval=price.interval,
            interval_count=price.interval_count,
            active=price.active,
            nickname=price.nickname,
            metadata=price.metadata
        )
        
        self.db.add(db_price)
        self.db.commit()
        self.db.refresh(db_price)
        
        return self._to_entity(db_price)
    
    async def get_price_by_stripe_id(self, stripe_price_id: str) -> Optional[StripePrice]:
        stmt = select(StripePriceModel).where(StripePriceModel.stripe_price_id == stripe_price_id)
        result = self.db.execute(stmt)
        db_price = result.scalar_one_or_none()
        
        if db_price:
            return self._to_entity(db_price)
        return None
    
    async def get_active_prices(self) -> List[StripePrice]:
        stmt = select(StripePriceModel).where(StripePriceModel.active == True)
        result = self.db.execute(stmt)
        db_prices = result.scalars().all()
        
        return [self._to_entity(price) for price in db_prices]
    
    async def update_price(self, price: StripePrice) -> StripePrice:
        stmt = select(StripePriceModel).where(StripePriceModel.stripe_price_id == price.stripe_price_id)
        result = self.db.execute(stmt)
        db_price = result.scalar_one_or_none()
        
        if db_price:
            db_price.active = price.active
            db_price.nickname = price.nickname
            db_price.metadata = price.metadata
            
            self.db.commit()
            self.db.refresh(db_price)
            return self._to_entity(db_price)
        
        raise ValueError("Price not found")
    
    def _to_entity(self, db_price: StripePriceModel) -> StripePrice:
        return StripePrice(
            id=str(db_price.id),
            stripe_price_id=db_price.stripe_price_id,
            stripe_product_id=db_price.stripe_product_id,
            amount=db_price.amount,
            currency=db_price.currency,
            interval=db_price.interval,
            interval_count=db_price.interval_count,
            active=db_price.active,
            nickname=db_price.nickname,
            metadata=db_price.metadata,
            created_at=db_price.created_at
        )