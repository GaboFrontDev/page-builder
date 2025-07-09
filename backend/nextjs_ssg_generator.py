import json
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Any
from models import Page, Component
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class NextJSSSGGenerator:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            self.output_dir = Path("/var/www/sites")
        else:
            self.output_dir = Path(output_dir)
        
        self.nextjs_dir = Path(__file__).parent / "nextjs-ssg"
        self.data_dir = self.nextjs_dir / "data"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _ensure_nextjs_built(self):
        """Ensure the Next.js system is built"""
        dist_dir = self.nextjs_dir / "dist"
        if not dist_dir.exists() or not self._verify_build():
            logger.info("Building Next.js SSG system...")
            subprocess.run(["npm", "run", "build"], cwd=self.nextjs_dir, check=True)
            
            if not self._verify_build():
                raise RuntimeError("Next.js build verification failed after build")
    
    def _verify_build(self):
        """Verify that the Next.js build completed successfully"""
        dist_dir = self.nextjs_dir / "dist"
        return dist_dir.exists() and (dist_dir / "index.html").exists()
    
    def _prepare_page_data(self, page: Page, db: Session) -> Dict[str, Any]:
        """Convert database models to JSON serializable format"""
        # Get components ordered by position
        components = db.query(Component).filter(
            Component.page_id == page.id,
            Component.is_visible == True
        ).order_by(Component.position).all()
        
        components_data = []
        for component in components:
            components_data.append({
                "id": component.id,
                "type": component.type,
                "content": component.content or {},
                "styles": component.styles or {},
                "position": component.position,
                "is_visible": component.is_visible
            })
        
        return {
            "id": page.id,
            "title": page.title,
            "description": page.description or "",
            "slug": page.slug,
            "subdomain": page.subdomain,
            "config": page.config or {},
            "components": components_data
        }
    
    def _generate_with_nextjs(self, page_data: Dict[str, Any]) -> str:
        """Use Next.js to generate the static page"""
        self._ensure_nextjs_built()
        
        # Write page data to JSON file
        data_file = self.data_dir / "page.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(page_data, f, indent=2)
        
        # Build the page with Next.js
        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.nextjs_dir,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Next.js build completed successfully")
            
            # Read the generated HTML
            html_file = self.nextjs_dir / "dist" / "index.html"
            with open(html_file, 'r', encoding='utf-8') as f:
                return f.read()
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Next.js build failed: {e.stderr}")
            raise RuntimeError(f"Next.js build failed: {e.stderr}")
    
    def generate_page(self, page: Page, db: Session) -> str:
        """Generate a complete page using Next.js SSG"""
        page_data = self._prepare_page_data(page, db)
        return self._generate_with_nextjs(page_data)
    
    def deploy_page(self, page: Page, db: Session) -> str:
        """Generate and deploy a page using Next.js SSG"""
        try:
            # Generate HTML
            html_content = self.generate_page(page, db)
            
            # Create directory for the subdomain if not exists
            subdomain_dir = self.output_dir / page.subdomain
            subdomain_dir.mkdir(parents=True, exist_ok=True)
            
            # Create directory for the page within the subdomain directory
            if page.slug and page.slug != "root":
                page_dir = subdomain_dir / page.slug
                page_dir.mkdir(parents=True, exist_ok=True)
            else:
                page_dir = subdomain_dir
            
            # Write HTML file
            html_file = page_dir / "index.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Copy Next.js assets
            self._copy_nextjs_assets(page_dir)
            
            if not self._verify_assets_copied(page_dir):
                raise RuntimeError("Asset copy verification failed")
                
            logger.info(f"Successfully deployed page {page.slug} to {page_dir}")
            return str(page_dir)
            
        except Exception as e:
            logger.error(f"Deployment failed for page {page.slug}: {e}")
            raise RuntimeError(f"Deployment failed: {e}")
    
    def _copy_nextjs_assets(self, target_dir: Path):
        """Copy assets from the Next.js build"""
        nextjs_assets = self.nextjs_dir / "dist" / "_next"
        if not nextjs_assets.exists():
            raise FileNotFoundError(f"Next.js assets not found at {nextjs_assets}")
        
        import shutil
        target_assets = target_dir / "_next"
        try:
            if target_assets.exists():
                shutil.rmtree(target_assets)
            shutil.copytree(nextjs_assets, target_assets)
            logger.info(f"Next.js assets copied from {nextjs_assets} to {target_assets}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to copy Next.js assets: {e}")
    
    def _verify_assets_copied(self, target_dir: Path):
        """Verify Next.js assets were copied correctly"""
        target_assets = target_dir / "_next"
        return target_assets.exists() and any(target_assets.iterdir())
    
    def delete_page(self, slug: str, subdomain: str = None):
        """Delete a deployed page"""
        if subdomain:
            if slug and slug != "root":
                page_dir = self.output_dir / subdomain / slug
            else:
                page_dir = self.output_dir / subdomain
                index_file = page_dir / "index.html"
                if index_file.exists():
                    index_file.unlink()
                    return True
                return False
        else:
            # Search in all subdomain directories
            page_dir = None
            for subdomain_dir in self.output_dir.iterdir():
                if subdomain_dir.is_dir():
                    if slug and slug != "root":
                        potential_page_dir = subdomain_dir / slug
                        if potential_page_dir.exists():
                            page_dir = potential_page_dir
                            break
                    else:
                        index_file = subdomain_dir / "index.html"
                        if index_file.exists():
                            index_file.unlink()
                            return True
            
            if page_dir and page_dir.exists():
                import shutil
                shutil.rmtree(page_dir)
                return True
            return False