from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict

from database import get_db
from models import Page, User
from generator import SiteGenerator
from auth import get_current_active_user

router = APIRouter(prefix="/api/deploy", tags=["deployment"])

# Instancia global del generador
generator = SiteGenerator()

@router.post("/{page_id}")
def deploy_page(
    page_id: int, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deploya una página específica (solo el propietario)"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Verificar que el usuario sea el propietario
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to deploy this page")
    
    if not page.is_published:
        raise HTTPException(status_code=400, detail="Page must be published before deployment")
    
    try:
        # Ejecutar deployment en background
        background_tasks.add_task(deploy_page_task, page, db)
        
        return {
            "message": "Deployment started",
            "page_id": page_id,
            "slug": page.slug,
            "url": f"http://{page.subdomain}.localhost/{page.slug}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@router.post("/slug/{slug}")
def deploy_page_by_slug(slug: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Deploya una página por slug"""
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    if not page.is_published:
        raise HTTPException(status_code=400, detail="Page must be published before deployment")
    
    try:
        background_tasks.add_task(deploy_page_task, page, db)
        
        return {
            "message": "Deployment started",
            "slug": slug,
            "url": f"http://{page.subdomain}.localhost/{slug}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@router.delete("/{page_id}")
def undeploy_page(page_id: int, db: Session = Depends(get_db)):
    """Elimina el deployment de una página"""
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    try:
        success = generator.delete_page(page.slug, page.subdomain)
        if success:
            return {"message": "Page undeployed successfully", "slug": page.slug}
        else:
            return {"message": "Page was not deployed", "slug": page.slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Undeployment failed: {str(e)}")

@router.delete("/slug/{slug}")
def undeploy_page_by_slug(
    slug: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Elimina el deployment de una página por slug (solo el propietario)"""
    # Verificar que la página existe y pertenece al usuario
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Verificar que el usuario sea el propietario
    if page.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to undeploy this page")
    
    try:
        success = generator.delete_page(slug, page.subdomain)
        if success:
            return {"message": "Page undeployed successfully", "slug": slug}
        else:
            return {"message": "Page was not deployed", "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Undeployment failed: {str(e)}")

@router.get("/status/{slug}")
def deployment_status(slug: str, db: Session = Depends(get_db)):
    """Verifica el estado del deployment de una página"""
    import os
    
    # Buscar la página para obtener el subdominio
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        return {
            "deployed": False,
            "slug": slug
        }
    
    page_dir = f"/var/www/sites/{page.subdomain}/{slug}"
    
    if os.path.exists(page_dir) and os.path.exists(f"{page_dir}/index.html"):
        return {
            "deployed": True,
            "slug": slug,
            "url": f"http://{page.subdomain}.localhost/{slug}",
            "path": page_dir
        }
    else:
        return {
            "deployed": False,
            "slug": slug
        }

@router.post("/rebuild-all")
def rebuild_all_sites(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Rebuilds todos los sitios publicados"""
    published_pages = db.query(Page).filter(Page.is_published == True).all()
    
    if not published_pages:
        return {"message": "No published pages found"}
    
    # Agregar tareas de rebuild para todas las páginas
    for page in published_pages:
        background_tasks.add_task(deploy_page_task, page, db)
    
    return {
        "message": f"Rebuild started for {len(published_pages)} pages",
        "pages": [{"id": p.id, "slug": p.slug} for p in published_pages]
    }

@router.get("/list")
def list_deployed_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista solo los sitios deployados del usuario actual"""
    import os
    sites_dir = "/var/www/sites"
    
    if not os.path.exists(sites_dir):
        return {"deployed_sites": []}
    
    deployed_sites = []
    
    # Obtener todas las páginas del usuario
    user_pages = db.query(Page).filter(Page.owner_id == current_user.id).all()
    
    for page in user_pages:
        # Buscar el directorio del subdominio
        subdomain_dir = os.path.join(sites_dir, page.subdomain)
        if os.path.exists(subdomain_dir):
            site_path = os.path.join(subdomain_dir, page.slug)
            if os.path.isdir(site_path) and os.path.exists(os.path.join(site_path, "index.html")):
                deployed_sites.append({
                    "slug": page.slug,
                    "url": f"http://{page.subdomain}.localhost/{page.slug}",
                    "path": site_path,
                    "is_owner": True,
                    "page_id": page.id,
                    "title": page.title
                })
    
    return {"deployed_sites": deployed_sites}

def deploy_page_task(page: Page, db: Session):
    """Tarea background para deployar una página"""
    try:
        # Crear una nueva sesión de DB para el background task
        from database import SessionLocal
        db_session = SessionLocal()
        
        # Re-fetch la página en la nueva sesión
        page_fresh = db_session.query(Page).filter(Page.id == page.id).first()
        if page_fresh:
            result_path = generator.deploy_page(page_fresh, db_session)
            print(f"Page deployed successfully: {page_fresh.slug} -> {result_path}")
        
        db_session.close()
    except Exception as e:
        print(f"Error deploying page {page.slug}: {str(e)}")
        raise