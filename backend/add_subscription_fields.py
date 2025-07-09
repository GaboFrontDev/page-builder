#!/usr/bin/env python3
"""
Script para agregar campos de suscripción a la tabla users
"""

from sqlalchemy import text
from database import engine

def add_subscription_fields():
    """Agregar campos subscription_active y stripe_customer_id a la tabla users"""
    
    with engine.connect() as conn:
        # Verificar si las columnas ya existen
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN ('subscription_active', 'stripe_customer_id')
        """))
        
        existing_columns = [row[0] for row in result.fetchall()]
        
        # Agregar subscription_active si no existe
        if 'subscription_active' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN subscription_active BOOLEAN NOT NULL DEFAULT FALSE
            """))
            print("✅ Columna subscription_active agregada")
        else:
            print("ℹ️ Columna subscription_active ya existe")
        
        # Agregar stripe_customer_id si no existe
        if 'stripe_customer_id' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN stripe_customer_id VARCHAR(255) NULL
            """))
            print("✅ Columna stripe_customer_id agregada")
        else:
            print("ℹ️ Columna stripe_customer_id ya existe")
        
        # Confirmar los cambios
        conn.commit()
        print("✅ Migración completada")

if __name__ == "__main__":
    add_subscription_fields()