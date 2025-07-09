import json
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Any
from models import Page, Component
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class ReactSSGGenerator:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            self.output_dir = Path("/var/www/sites")
        else:
            self.output_dir = Path(output_dir)
        
        self.ssg_dir = Path(__file__).parent / "ssg"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _ensure_ssg_built(self):
        """Ensure the SSG system is built"""
        dist_dir = self.ssg_dir / "dist"
        if not dist_dir.exists() or not self._verify_build():
            logger.info("Building SSG system...")
            subprocess.run(["npm", "run", "build"], cwd=self.ssg_dir, check=True)
            
            if not self._verify_build():
                raise RuntimeError("SSG build verification failed after build")
    
    def _verify_build(self):
        """Verify that the build completed successfully"""
        dist_dir = self.ssg_dir / "dist" / "assets"
        required_files = ["style.css", "main.js"]
        
        for file in required_files:
            file_path = dist_dir / file
            if not file_path.exists():
                logger.error(f"Required asset {file} not found at {file_path}")
                return False
            if file_path.stat().st_size == 0:
                logger.error(f"Required asset {file} is empty")
                return False
        return True
    
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
    
    def _render_with_node(self, page_data: Dict[str, Any]) -> str:
        """Use Node.js to render the React page to HTML"""
        self._ensure_ssg_built()
        
        # Create a temporary file with the page data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(page_data, f)
            temp_file = f.name
        
        try:
            # Create a Node.js script to render the page
            node_script = f"""
const fs = require('fs');
const path = require('path');

// Load the built SSG bundle
require('{self.ssg_dir}/dist/assets/main.js');

// Read page data
const pageData = JSON.parse(fs.readFileSync('{temp_file}', 'utf8'));

// Render the page
const html = global.renderPageToHTML(pageData);

// Output the HTML
console.log(html);
"""
            
            # Write the Node.js script to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as script_file:
                script_file.write(node_script)
                script_path = script_file.name
            
            # Run the Node.js script
            result = subprocess.run(
                ["node", script_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip()
            
        finally:
            # Clean up temporary files
            Path(temp_file).unlink(missing_ok=True)
            Path(script_path).unlink(missing_ok=True)
    
    def generate_page(self, page: Page, db: Session) -> str:
        """Generate a complete page using React SSG"""
        page_data = self._prepare_page_data(page, db)
        return self._render_with_node(page_data)
    
    def deploy_page(self, page: Page, db: Session) -> str:
        """Generate and deploy a page using React SSG"""
        try:
            # Ensure SSG is built with fresh assets before deployment
            self._ensure_ssg_built()
            
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
            
            # Copy assets and verify
            self._copy_assets(page_dir)
            
            if not self._verify_assets_copied(page_dir):
                raise RuntimeError("Asset copy verification failed")
                
            logger.info(f"Successfully deployed page {page.slug} to {page_dir}")
            return str(page_dir)
            
        except Exception as e:
            logger.error(f"Deployment failed for page {page.slug}: {e}")
            raise RuntimeError(f"Deployment failed: {e}")
    
    def _copy_assets(self, target_dir: Path):
        """Copy assets from the SSG build"""
        ssg_assets = self.ssg_dir / "dist" / "assets"
        if not ssg_assets.exists():
            raise FileNotFoundError(f"SSG assets not found at {ssg_assets}")
        
        import shutil
        target_assets = target_dir / "assets"
        try:
            if target_assets.exists():
                shutil.rmtree(target_assets)
            shutil.copytree(ssg_assets, target_assets)
            logger.info(f"Assets copied from {ssg_assets} to {target_assets}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to copy assets: {e}")
    
    def _verify_assets_copied(self, target_dir: Path):
        """Verify assets were copied correctly"""
        target_assets = target_dir / "assets"
        source_assets = self.ssg_dir / "dist" / "assets"
        
        for asset in ["style.css", "main.js"]:
            source_file = source_assets / asset
            target_file = target_assets / asset
            
            if not target_file.exists():
                logger.error(f"Asset {asset} not found at {target_file}")
                return False
            if source_file.stat().st_size != target_file.stat().st_size:
                logger.error(f"Asset {asset} size mismatch: source={source_file.stat().st_size}, target={target_file.stat().st_size}")
                return False
        return True
    
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