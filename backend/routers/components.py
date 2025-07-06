from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Component, Page, User
from schemas import Component as ComponentSchema, ComponentCreate, ComponentUpdate, ComponentReorder
from auth import get_current_active_user

router = APIRouter(prefix="/api/components", tags=["components"])

def verify_page_ownership(page_id: int, current_user: User, db: Session):
    """Verifica que el usuario sea propietario de la página"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this page")
    return page

@router.get("/page/{page_id}", response_model=List[ComponentSchema])
def get_page_components(
    page_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener componentes de una página (solo el propietario)"""
    verify_page_ownership(page_id, current_user, db)
    components = db.query(Component).filter(Component.page_id == page_id).order_by(Component.position).all()
    return components

@router.get("/{component_id}", response_model=ComponentSchema)
def get_component(
    component_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un componente específico (solo el propietario de la página)"""
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Verificar que el usuario sea propietario de la página
    verify_page_ownership(component.page_id, current_user, db)
    return component

@router.post("/", response_model=ComponentSchema)
def create_component(
    component: ComponentCreate, 
    page_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear un componente (solo el propietario de la página)"""
    verify_page_ownership(page_id, current_user, db)
    
    db_component = Component(
        type=component.type,
        content=component.content,
        styles=component.styles,
        position=component.position,
        is_visible=component.is_visible,
        page_id=page_id
    )
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

@router.put("/{component_id}", response_model=ComponentSchema)
def update_component(
    component_id: int, 
    component_update: ComponentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar un componente (solo el propietario de la página)"""
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Verificar que el usuario sea propietario de la página
    verify_page_ownership(component.page_id, current_user, db)
    
    # Solo actualizar campos que no sean None
    update_data = component_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(component, field, value)
    
    db.commit()
    db.refresh(component)
    return component

@router.delete("/{component_id}")
def delete_component(
    component_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un componente (solo el propietario de la página)"""
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Verificar que el usuario sea propietario de la página
    verify_page_ownership(component.page_id, current_user, db)
    
    db.delete(component)
    db.commit()
    return {"message": "Component deleted successfully"}

@router.post("/reorder")
def reorder_components(
    reorder_data: ComponentReorder,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reordenar componentes de una página (solo el propietario)"""
    verify_page_ownership(reorder_data.page_id, current_user, db)
    
    # Verificar que todos los componentes pertenezcan a la página
    components = db.query(Component).filter(
        Component.id.in_(reorder_data.component_ids),
        Component.page_id == reorder_data.page_id
    ).all()
    
    if len(components) != len(reorder_data.component_ids):
        raise HTTPException(status_code=400, detail="Some components not found or don't belong to this page")
    
    # Actualizar posiciones
    for i, component_id in enumerate(reorder_data.component_ids):
        component = next(c for c in components if c.id == component_id)
        component.position = i
    
    db.commit()
    return components

@router.post("/{component_id}/reorder")
def reorder_component(
    component_id: int, 
    new_position: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reordenar un componente específico (solo el propietario de la página)"""
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Verificar que el usuario sea propietario de la página
    verify_page_ownership(component.page_id, current_user, db)
    
    old_position = component.position
    page_id = component.page_id
    
    # Actualizar posiciones de otros componentes
    if new_position > old_position:
        # Mover hacia abajo
        db.query(Component).filter(
            Component.page_id == page_id,
            Component.position > old_position,
            Component.position <= new_position
        ).update({Component.position: Component.position - 1})
    else:
        # Mover hacia arriba
        db.query(Component).filter(
            Component.page_id == page_id,
            Component.position >= new_position,
            Component.position < old_position
        ).update({Component.position: Component.position + 1})
    
    component.position = new_position
    db.commit()
    db.refresh(component)
    return component