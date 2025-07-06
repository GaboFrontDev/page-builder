#!/usr/bin/env python3
"""
Script para probar la restricción única de subdomain+slug
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, Page, User
from sqlalchemy.exc import IntegrityError

# Usar SQLite para las pruebas
DATABASE_URL = "sqlite:///test_unique_constraint.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_unique_constraint():
    """Probar que la restricción única subdomain+slug funciona"""
    
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear un usuario de prueba
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Crear primera página
        page1 = Page(
            title="Página 1",
            slug="pagina1",
            subdomain="test",
            description="Primera página de prueba",
            owner_id=test_user.id
        )
        db.add(page1)
        db.commit()
        print("✅ Primera página creada exitosamente")
        
        # Intentar crear segunda página con misma combinación subdomain+slug
        page2 = Page(
            title="Página 2",
            slug="pagina1",  # Mismo slug
            subdomain="test",  # Mismo subdomain
            description="Segunda página de prueba (debería fallar)",
            owner_id=test_user.id
        )
        db.add(page2)
        db.commit()
        print("❌ ERROR: Se permitió crear página duplicada")
        return False
        
    except IntegrityError as e:
        print("✅ Restricción única funcionando correctamente")
        print(f"Error capturado: {e}")
        db.rollback()
        
        # Probar que diferentes combinaciones funcionan
        try:
            # Diferente slug, mismo subdomain
            page3 = Page(
                title="Página 3",
                slug="pagina2",
                subdomain="test",
                description="Tercera página de prueba",
                owner_id=test_user.id
            )
            db.add(page3)
            db.commit()
            print("✅ Página con diferente slug creada exitosamente")
            
            # Mismo slug, diferente subdomain
            page4 = Page(
                title="Página 4",
                slug="pagina1",
                subdomain="test2",
                description="Cuarta página de prueba",
                owner_id=test_user.id
            )
            db.add(page4)
            db.commit()
            print("✅ Página con diferente subdomain creada exitosamente")
            
            print("\n🎉 Todas las pruebas de restricción única pasaron correctamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error en pruebas adicionales: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        db.close()
        # Limpiar archivo de prueba
        if os.path.exists("test_unique_constraint.db"):
            os.remove("test_unique_constraint.db")

if __name__ == "__main__":
    success = test_unique_constraint()
    sys.exit(0 if success else 1) 