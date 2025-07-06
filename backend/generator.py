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
    
    def _convert_styles_to_tailwind(self, styles: str) -> str:
        """Convierte estilos CSS a clases de Tailwind"""
        if not styles:
            return ""
        
        # Mapeo básico de estilos CSS a clases de Tailwind
        style_mappings = {
            "background-color: #007bff": "bg-primary",
            "background-color: #6c757d": "bg-secondary",
            "background-color: #28a745": "bg-success",
            "background-color: #dc3545": "bg-danger",
            "color: white": "text-white",
            "color: #333": "text-gray-900",
            "color: #666": "text-gray-600",
            "text-align: center": "text-center",
            "text-align: left": "text-left",
            "text-align: right": "text-right",
            "padding: 20px": "p-5",
            "padding: 40px 20px": "py-10 px-5",
            "margin-bottom: 20px": "mb-5",
            "margin-top: 20px": "mt-5",
            "font-weight: bold": "font-bold",
            "font-size: 1.5rem": "text-2xl",
            "font-size: 3rem": "text-5xl",
            "font-size: 1.2rem": "text-xl",
            "border-radius: 5px": "rounded",
            "border-radius: 8px": "rounded-lg",
            "display: flex": "flex",
            "justify-content: space-between": "justify-between",
            "align-items: center": "items-center",
        }
        
        tailwind_classes = []
        for css_style in styles.split(";"):
            css_style = css_style.strip()
            if css_style in style_mappings:
                tailwind_classes.append(style_mappings[css_style])
        
        return " ".join(tailwind_classes)
    
    def _generate_hero(self, content: Dict, styles: str) -> str:
        title = content.get("title", "")
        subtitle = content.get("subtitle", "")
        image = content.get("image", "")
        cta_text = content.get("cta_text", "")
        cta_link = content.get("cta_link", "#")
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        
        html = f'''
        <section class="hero text-center py-20 px-4 {tailwind_classes}">
            {f'<img src="{image}" alt="Hero" class="max-w-full h-auto mb-8 rounded-lg">' if image else ''}
            <h1 class="text-5xl font-bold mb-6 text-gray-900 dark:text-white">{title}</h1>
            <p class="text-xl mb-8 text-gray-600 dark:text-gray-300">{subtitle}</p>
            {f'<a href="{cta_link}" class="bg-primary hover:bg-primary/90 text-white px-8 py-4 rounded-lg font-semibold inline-block transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-lg">{cta_text}</a>' if cta_text else ''}
        </section>
        '''
        return html
    
    def _generate_text(self, content: Dict, styles: str) -> str:
        text = content.get("text", "")
        alignment = content.get("alignment", "left")
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        alignment_class = "text-center" if alignment == "center" else "text-left" if alignment == "left" else "text-right"
        
        html = f'''
        <section class="text-section py-10 px-5 {alignment_class} {tailwind_classes}">
            <div class="max-w-4xl mx-auto">
                {text}
            </div>
        </section>
        '''
        return html
    
    def _generate_image(self, content: Dict, styles: str) -> str:
        src = content.get("src", "")
        alt = content.get("alt", "")
        caption = content.get("caption", "")
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        
        html = f'''
        <section class="image-section py-10 px-5 text-center {tailwind_classes}">
            <img src="{src}" alt="{alt}" class="max-w-full h-auto rounded-lg shadow-lg">
            {f'<p class="mt-4 italic text-gray-600 dark:text-gray-400">{caption}</p>' if caption else ''}
        </section>
        '''
        return html
    
    def _generate_button(self, content: Dict, styles: str) -> str:
        text = content.get("text", "Click me")
        link = content.get("link", "#")
        variant = content.get("variant", "primary")
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        
        # Clases de botón según variante
        button_classes = {
            "primary": "bg-primary hover:bg-primary/90 text-white",
            "secondary": "bg-secondary hover:bg-secondary/90 text-white",
            "outline": "bg-transparent text-primary border-2 border-primary hover:bg-primary hover:text-white"
        }
        
        html = f'''
        <section class="button-section p-5 text-center {tailwind_classes}">
            <a href="{link}" class="{button_classes.get(variant, button_classes['primary'])} px-8 py-4 rounded-lg font-semibold inline-block transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-lg">
                {text}
            </a>
        </section>
        '''
        return html
    
    def _generate_header(self, content: Dict, styles: str) -> str:
        title = content.get("title", "")
        logo = content.get("logo", "")
        menu_items = content.get("menu_items", [])
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        
        menu_html = ""
        if menu_items:
            menu_html = '<nav class="inline-block">'
            for item in menu_items:
                menu_html += f'<a href="{item.get("link", "#")}" class="ml-5 text-gray-900 dark:text-white hover:text-primary transition-colors duration-200">{item.get("text", "")}</a>'
            menu_html += "</nav>"
        
        html = f'''
        <header class="p-5 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center {tailwind_classes}">
            <div class="flex items-center">
                {f'<img src="{logo}" alt="Logo" class="h-10 mr-4">' if logo else ''}
                <h1 class="m-0 text-2xl font-bold text-gray-900 dark:text-white">{title}</h1>
            </div>
            {menu_html}
        </header>
        '''
        return html
    
    def _generate_footer(self, content: Dict, styles: str) -> str:
        text = content.get("text", "")
        links = content.get("links", [])
        
        # Convertir estilos a clases de Tailwind
        tailwind_classes = self._convert_styles_to_tailwind(styles)
        
        links_html = ""
        if links:
            links_html = '<div class="mt-5">'
            for link in links:
                links_html += f'<a href="{link.get("url", "#")}" class="mr-5 text-gray-600 dark:text-gray-400 hover:text-primary transition-colors duration-200">{link.get("text", "")}</a>'
            links_html += "</div>"
        
        html = f'''
        <footer class="py-10 px-5 text-center border-t border-gray-200 dark:border-gray-700 mt-10 {tailwind_classes}">
            <p class="m-0 text-gray-600 dark:text-gray-400">{text}</p>
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