from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_active = Column(Boolean, default=False)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    pages = relationship("Page", back_populates="owner")
    # Relaciones con Stripe - Temporalmente comentadas para evitar errores
    # subscription = relationship("SubscriptionModel", back_populates="user", uselist=False)
    # customer = relationship("CustomerModel", back_populates="user", uselist=False)
    # user_extension = relationship("UserExtensionModel", back_populates="user", uselist=False)

class Page(Base):
    __tablename__ = "pages"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, index=True)  # Ya no es único por sí solo
    subdomain = Column(String, index=True)  # Ya no es único por sí solo
    description = Column(Text)
    config = Column(JSON)  # Configuración completa de la página
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="pages")
    components = relationship("Component", back_populates="page")

    __table_args__ = (
        # Índice único compuesto
        UniqueConstraint('subdomain', 'slug', name='uq_subdomain_slug'),
    )

class Component(Base):
    __tablename__ = "components"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # header, hero, text, image, button, etc.
    content = Column(JSON)  # Contenido específico del componente
    styles = Column(JSON)  # Estilos CSS
    position = Column(Integer)  # Orden en la página
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    page_id = Column(Integer, ForeignKey("pages.id"))
    page = relationship("Page", back_populates="components")

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    thumbnail = Column(String)  # URL de la imagen preview
    config = Column(JSON)  # Configuración base del template
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    original_name = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User")