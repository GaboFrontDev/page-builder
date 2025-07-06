from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import os
import json
from typing import Dict, List, Any
from models import Page, Component
from sqlalchemy.orm import Session
from models import User

class SiteGenerator:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            # Usar el directorio estándar para nginx
            self.output_dir = Path("/var/www/sites")
        else:
            self.output_dir = Path(output_dir)
        
        self.templates_dir = Path(__file__).parent / "templates"
        
        # Configurar Jinja2
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Asegurar que el directorio existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_component_html(self, component: Component) -> str:
        """Genera HTML para un componente específico"""
        component_type = component.type
        content = component.content
        styles = component.styles or {}
        
        # Convertir estilos a CSS
        css_styles = self._dict_to_css(styles)
        
        if component_type == "hero":
            return self._generate_hero(content, css_styles)
        elif component_type == "text":
            return self._generate_text(content, css_styles)
        elif component_type == "image":
            return self._generate_image(content, css_styles)
        elif component_type == "button":
            return self._generate_button(content, css_styles)
        elif component_type == "header":
            return self._generate_header(content, css_styles)
        elif component_type == "footer":
            return self._generate_footer(content, css_styles)
        else:
            return f'<div class="component-{component_type}" style="{css_styles}">Componente no implementado: {component_type}</div>'
    
    def _dict_to_css(self, styles: Dict[str, Any]) -> str:
        """Convierte un diccionario de estilos a CSS"""
        css_rules = []
        for key, value in styles.items():
            # Saltar claves None o vacías
            if key is None or key == "":
                continue
            # Convertir camelCase a kebab-case
            css_key = ''.join(['-' + c.lower() if c.isupper() else c for c in str(key)]).lstrip('-')
            css_rules.append(f"{css_key}: {value}")
        return "; ".join(css_rules)
    
    def _generate_hero(self, content: Dict, styles: str) -> str:
        title = content.get("title", "")
        subtitle = content.get("subtitle", "")
        image = content.get("image", "")
        cta_text = content.get("cta_text", "")
        cta_link = content.get("cta_link", "#")
        
        html = f'''
        <section class="hero" style="text-align: center; padding: 80px 20px; {styles}">
            {f'<img src="{image}" alt="Hero" style="max-width: 100%; height: auto; margin-bottom: 30px;">' if image else ''}
            <h1 style="font-size: 3rem; margin-bottom: 20px; color: #333;">{title}</h1>
            <p style="font-size: 1.2rem; margin-bottom: 30px; color: #666;">{subtitle}</p>
            {f'<a href="{cta_link}" style="background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">{cta_text}</a>' if cta_text else ''}
        </section>
        '''
        return html
    
    def _generate_text(self, content: Dict, styles: str) -> str:
        text = content.get("text", "")
        alignment = content.get("alignment", "left")
        
        html = f'''
        <section class="text-section" style="padding: 40px 20px; text-align: {alignment}; {styles}">
            <div style="max-width: 800px; margin: 0 auto;">
                {text}
            </div>
        </section>
        '''
        return html
    
    def _generate_image(self, content: Dict, styles: str) -> str:
        src = content.get("src", "")
        alt = content.get("alt", "")
        caption = content.get("caption", "")
        
        html = f'''
        <section class="image-section" style="padding: 40px 20px; text-align: center; {styles}">
            <img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 8px;">
            {f'<p style="margin-top: 15px; font-style: italic; color: #666;">{caption}</p>' if caption else ''}
        </section>
        '''
        return html
    
    def _generate_button(self, content: Dict, styles: str) -> str:
        text = content.get("text", "Click me")
        link = content.get("link", "#")
        variant = content.get("variant", "primary")
        
        button_styles = {
            "primary": "background: #007bff; color: white;",
            "secondary": "background: #6c757d; color: white;",
            "outline": "background: transparent; color: #007bff; border: 2px solid #007bff;"
        }
        
        html = f'''
        <section class="button-section" style="padding: 20px; text-align: center; {styles}">
            <a href="{link}" style="{button_styles.get(variant, button_styles['primary'])} padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                {text}
            </a>
        </section>
        '''
        return html
    
    def _generate_header(self, content: Dict, styles: str) -> str:
        title = content.get("title", "")
        logo = content.get("logo", "")
        menu_items = content.get("menu_items", [])
        
        menu_html = ""
        if menu_items:
            menu_html = "<nav style='display: inline-block;'>"
            for item in menu_items:
                menu_html += f'<a href="{item.get("link", "#")}" style="margin-left: 20px; text-decoration: none; color: #333;">{item.get("text", "")}</a>'
            menu_html += "</nav>"
        
        html = f'''
        <header style="padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; {styles}">
            <div style="display: flex; align-items: center;">
                {f'<img src="{logo}" alt="Logo" style="height: 40px; margin-right: 15px;">' if logo else ''}
                <h1 style="margin: 0; font-size: 1.5rem;">{title}</h1>
            </div>
            {menu_html}
        </header>
        '''
        return html
    
    def _generate_footer(self, content: Dict, styles: str) -> str:
        text = content.get("text", "")
        links = content.get("links", [])
        
        links_html = ""
        if links:
            links_html = "<div style='margin-top: 20px;'>"
            for link in links:
                links_html += f'<a href="{link.get("url", "#")}" style="margin-right: 20px; text-decoration: none; color: #666;">{link.get("text", "")}</a>'
            links_html += "</div>"
        
        html = f'''
        <footer style="padding: 40px 20px; text-align: center; border-top: 1px solid #eee; margin-top: 40px; {styles}">
            <p style="margin: 0; color: #666;">{text}</p>
            {links_html}
        </footer>
        '''
        return html
    
    def generate_page(self, page: Page, db: Session) -> str:
        """Genera una página completa"""
        # Obtener componentes ordenados por posición
        components = db.query(Component).filter(
            Component.page_id == page.id,
            Component.is_visible == True
        ).order_by(Component.position).all()
        
        # Generar HTML de componentes
        components_html = ""
        for component in components:
            components_html += self.generate_component_html(component)
        
        # Obtener configuración de la página
        config = page.config or {}
        theme = config.get("theme", "default")
        
        # Usar template base
        template = self.env.get_template("base.html")
        
        return template.render(
            title=page.title,
            description=page.description,
            content=components_html,
            theme=theme,
            slug=page.slug
        )
    
    def deploy_page(self, page: Page, db: Session) -> str:
        """Genera y deploya una página"""
        # Generar HTML
        html_content = self.generate_page(page, db)
        
        # Crear directorio para el subdominio si no existe
        subdomain_dir = self.output_dir / page.subdomain
        subdomain_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear directorio para la página dentro del directorio del subdominio
        # Para páginas root (slug vacío o "root"), usar el directorio del subdominio directamente
        if page.slug and page.slug != "root":
            page_dir = subdomain_dir / page.slug
            page_dir.mkdir(parents=True, exist_ok=True)
        else:
            page_dir = subdomain_dir
        
        # Escribir archivo HTML
        html_file = page_dir / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Copiar assets si existen
        self._copy_assets(page_dir)
        
        return str(page_dir)
    
    def _copy_assets(self, target_dir: Path):
        """Copia assets comunes (CSS, JS, imágenes)"""
        assets_dir = self.templates_dir / "assets"
        if assets_dir.exists():
            import shutil
            target_assets = target_dir / "assets"
            if target_assets.exists():
                shutil.rmtree(target_assets)
            shutil.copytree(assets_dir, target_assets)
    
    def delete_page(self, slug: str, subdomain: str = None):
        """Elimina una página deployada"""
        if subdomain:
            # Si se proporciona subdomain, buscar en el directorio del subdominio
            if slug and slug != "root":
                page_dir = self.output_dir / subdomain / slug
            else:
                # Para páginas root, eliminar el index.html del directorio del subdominio
                page_dir = self.output_dir / subdomain
                index_file = page_dir / "index.html"
                if index_file.exists():
                    index_file.unlink()
                    return True
                return False
        else:
            # Buscar en todos los directorios de subdominios
            page_dir = None
            for subdomain_dir in self.output_dir.iterdir():
                if subdomain_dir.is_dir():
                    if slug and slug != "root":
                        potential_page_dir = subdomain_dir / slug
                        if potential_page_dir.exists():
                            page_dir = potential_page_dir
                            break
                    else:
                        # Para páginas root, buscar index.html en el directorio del subdominio
                        index_file = subdomain_dir / "index.html"
                        if index_file.exists():
                            index_file.unlink()
                            return True
            
            if page_dir and page_dir.exists():
                import shutil
                shutil.rmtree(page_dir)
                return True
            return False 