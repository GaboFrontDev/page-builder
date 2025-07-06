from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Component
from schemas import Component as ComponentSchema, ComponentCreate

router = APIRouter(prefix="/api/components", tags=["components"])

@router.get("/page/{page_id}", response_model=List[ComponentSchema])
def get_page_components(page_id: int, db: Session = Depends(get_db)):
    components = db.query(Component).filter(Component.page_id == page_id).order_by(Component.position).all()
    return components

@router.get("/{component_id}", response_model=ComponentSchema)
def get_component(component_id: int, db: Session = Depends(get_db)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component

@router.post("/", response_model=ComponentSchema)
def create_component(component: ComponentCreate, page_id: int, db: Session = Depends(get_db)):
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
def update_component(component_id: int, component_update: ComponentCreate, db: Session = Depends(get_db)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    for field, value in component_update.dict().items():
        setattr(component, field, value)
    
    db.commit()
    db.refresh(component)
    return component

@router.delete("/{component_id}")
def delete_component(component_id: int, db: Session = Depends(get_db)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    db.delete(component)
    db.commit()
    return {"message": "Component deleted successfully"}

@router.post("/{component_id}/reorder")
def reorder_component(component_id: int, new_position: int, db: Session = Depends(get_db)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
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