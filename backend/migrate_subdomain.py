#!/usr/bin/env python3
"""
Script para migrar páginas existentes agregando subdomains por defecto
"""

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Page, User
import re

def generate_subdomain(title: str, user_id: int, page_id: int) -> str:
    """Genera un subdomain basado en el título de la página"""
    # Limpiar el título para crear un subdomain válido
    subdomain = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    subdomain = re.sub(r'\s+', '-', subdomain)
    subdomain = subdomain.strip('-')
    
    # Si está vacío o es muy corto, usar un fallback
    if not subdomain or len(subdomain) < 3:
        subdomain = f"pagina-{page_id}"
    
    return subdomain

def migrate_pages():
    """Migra todas las páginas existentes agregando subdomains"""
    db = SessionLocal()
    
    try:
        # Obtener todas las páginas que no tienen subdomain
        pages_without_subdomain = db.query(Page).filter(Page.subdomain.is_(None)).all()
        
        print(f"Encontradas {len(pages_without_subdomain)} páginas sin subdomain")
        
        for page in pages_without_subdomain:
            # Generar subdomain único
            base_subdomain = generate_subdomain(page.title, page.owner_id, page.id)
            subdomain = base_subdomain
            
            # Verificar que el subdomain sea único
            counter = 1
            while db.query(Page).filter(Page.subdomain == subdomain).first():
                subdomain = f"{base_subdomain}-{counter}"
                counter += 1
            
            # Actualizar la página
            page.subdomain = subdomain
            print(f"Página '{page.title}' (ID: {page.id}) -> subdomain: {subdomain}")
        
        # Confirmar cambios
        db.commit()
        print("Migración completada exitosamente")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_pages() 