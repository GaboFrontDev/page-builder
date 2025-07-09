from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ...domain.entities import StripeSubscriptionStatus, StripeEventType

Base = declarative_base()


class StripeCustomerModel(Base):
    __tablename__ = "stripe_customers"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_customer_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    phone = Column(String)
    stripe_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    subscriptions = relationship("StripeSubscriptionModel", back_populates="customer")
    payment_methods = relationship("StripePaymentMethodModel", back_populates="customer")


class StripeSubscriptionModel(Base):
    __tablename__ = "stripe_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_subscription_id = Column(String, unique=True, index=True)
    stripe_customer_id = Column(String, ForeignKey("stripe_customers.stripe_customer_id"))
    stripe_price_id = Column(String, index=True)
    status = Column(Enum(StripeSubscriptionStatus))
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    canceled_at = Column(DateTime)
    trial_start = Column(DateTime)
    trial_end = Column(DateTime)
    stripe_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    customer = relationship("StripeCustomerModel", back_populates="subscriptions")


class StripePaymentMethodModel(Base):
    __tablename__ = "stripe_payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_payment_method_id = Column(String, unique=True, index=True)
    stripe_customer_id = Column(String, ForeignKey("stripe_customers.stripe_customer_id"))
    type = Column(String)
    card_last4 = Column(String)
    card_brand = Column(String)
    card_exp_month = Column(Integer)
    card_exp_year = Column(Integer)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    customer = relationship("StripeCustomerModel", back_populates="payment_methods")


class StripeTransactionModel(Base):
    __tablename__ = "stripe_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_event_id = Column(String, unique=True, index=True)
    event_type = Column(Enum(StripeEventType))
    object_id = Column(String, index=True)
    amount = Column(Integer)  # En centavos
    currency = Column(String)
    status = Column(String)
    stripe_metadata = Column(JSON)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class StripePriceModel(Base):
    __tablename__ = "stripe_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_price_id = Column(String, unique=True, index=True)
    stripe_product_id = Column(String, index=True)
    amount = Column(Integer)  # En centavos
    currency = Column(String)
    interval = Column(String)
    interval_count = Column(Integer)
    active = Column(Boolean, default=True)
    nickname = Column(String)
    stripe_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)