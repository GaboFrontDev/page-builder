#!/usr/bin/env python3
"""
Script para eliminar el índice único del campo slug que está causando conflictos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from database import DATABASE_URL

def remove_slug_unique_index():
    """Elimina el índice único del campo slug"""
    
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        try:
            # Verificar si el índice existe
            result = connection.execute(text("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'pages' AND indexname = 'ix_pages_slug'
            """))
            
            index_exists = result.fetchone()
            if not index_exists:
                print("✅ El índice único 'ix_pages_slug' no existe")
                return True
            
            print(f"🔍 Encontrado índice: {index_exists[0]}")
            print(f"   Definición: {index_exists[1]}")
            
            # Eliminar el índice único
            connection.execute(text("DROP INDEX IF EXISTS ix_pages_slug"))
            connection.commit()
            
            print("✅ Índice único 'ix_pages_slug' eliminado exitosamente")
            
            # Verificar que se eliminó
            result = connection.execute(text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = 'pages' AND indexname = 'ix_pages_slug'
            """))
            
            if not result.fetchone():
                print("✅ Confirmado: el índice único ha sido eliminado")
                return True
            else:
                print("❌ Error: el índice aún existe")
                return False
                
        except Exception as e:
            print(f"❌ Error al eliminar el índice: {e}")
            return False

if __name__ == "__main__":
    print("🔄 Eliminando índice único del campo slug...")
    success = remove_slug_unique_index()
    if success:
        print("🎉 Migración completada exitosamente")
    else:
        print("❌ Migración falló")
        sys.exit(1) 