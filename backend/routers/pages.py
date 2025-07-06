from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Page, Component, User
from schemas import Page as PageSchema, PageCreate, PageUpdate, Component as ComponentSchema
from auth import get_current_active_user, get_current_user_optional

router = APIRouter(prefix="/api/pages", tags=["pages"])

@router.get("/", response_model=List[PageSchema])
def get_pages(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """Obtener páginas (públicas o del usuario si está autenticado)"""
    query = db.query(Page)
    
    if current_user:
        # Usuario autenticado: ver sus páginas + páginas públicas
        query = query.filter(
            (Page.owner_id == current_user.id) | 
            (Page.is_published == True)
        )
    else:
        # Usuario no autenticado: solo páginas públicas
        query = query.filter(Page.is_published == True)
    
    pages = query.offset(skip).limit(limit).all()
    return pages

@router.get("/{page_id}", response_model=PageSchema)
def get_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/slug/{slug}", response_model=PageSchema)
def get_page_by_slug(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.post("/", response_model=PageSchema)
def create_page(
    page: PageCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear una nueva página (requiere autenticación)"""
    # Verificar que el slug no exista
    existing_page = db.query(Page).filter(Page.slug == page.slug).first()
    if existing_page:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    db_page = Page(
        title=page.title,
        slug=page.slug,
        description=page.description,
        config=page.config,
        is_published=page.is_published,
        owner_id=current_user.id
    )
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

@router.put("/{page_id}", response_model=PageSchema)
def update_page(
    page_id: int, 
    page_update: PageUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar página (solo el propietario)"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Verificar que el usuario sea el propietario
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this page")
    
    for field, value in page_update.dict(exclude_unset=True).items():
        setattr(page, field, value)
    
    db.commit()
    db.refresh(page)
    return page

@router.delete("/{page_id}")
def delete_page(
    page_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar página (solo el propietario)"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Verificar que el usuario sea el propietario
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this page")
    
    db.delete(page)
    db.commit()
    return {"message": "Page deleted successfully"}

@router.post("/{page_id}/publish")
def publish_page(
    page_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Publicar página (solo el propietario)"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Verificar que el usuario sea el propietario
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to publish this page")
    
    page.is_published = True
    db.commit()
    db.refresh(page)
    return {"message": "Page published successfully", "page": page}