#!/usr/bin/env python3
"""
Script para migrar páginas con slug vacío a usar 'root' como slug
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Page
from database import DATABASE_URL

def migrate_root_pages():
    """Migra páginas con slug vacío a usar 'root' como slug"""
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Buscar páginas con slug vacío
        root_pages = db.query(Page).filter(Page.slug == "").all()
        
        print(f"Encontradas {len(root_pages)} páginas con slug vacío")
        
        for page in root_pages:
            print(f"Migrando página ID {page.id}: {page.title} (subdomain: {page.subdomain})")
            
            # Verificar si ya existe una página con slug 'root' en el mismo subdomain
            existing_root = db.query(Page).filter(
                Page.subdomain == page.subdomain,
                Page.slug == "root"
            ).first()
            
            if existing_root:
                print(f"  ⚠️  Ya existe una página root en subdomain '{page.subdomain}', usando slug único")
                # Usar un slug único basado en el ID
                page.slug = f"root-{page.id}"
            else:
                print(f"  ✅ Cambiando slug de '' a 'root'")
                page.slug = "root"
        
        # Commit de los cambios
        db.commit()
        print(f"✅ Migración completada. {len(root_pages)} páginas actualizadas")
        
        # Mostrar resumen
        print("\nResumen de páginas root:")
        root_pages_after = db.query(Page).filter(Page.slug.like("root%")).all()
        for page in root_pages_after:
            print(f"  - ID {page.id}: {page.title} (subdomain: {page.subdomain}, slug: {page.slug})")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("🔄 Iniciando migración de páginas root...")
    success = migrate_root_pages()
    if success:
        print("🎉 Migración completada exitosamente")
    else:
        print("❌ Migración falló")
        sys.exit(1) 