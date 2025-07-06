import pytest
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from generator import SiteGenerator
from models import Page, Component
from database import SessionLocal


class TestSiteGenerator:
    
    @pytest.fixture
    def temp_output_dir(self):
        """Directorio temporal para tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def generator(self, temp_output_dir):
        """Instancia del generador con directorio temporal"""
        return SiteGenerator(output_dir=temp_output_dir)
    
    @pytest.fixture
    def mock_page(self):
        """Mock de una página"""
        page = Mock(spec=Page)
        page.id = 1
        page.title = "Test Page"
        page.slug = "test-page"
        page.subdomain = "test"
        page.description = "A test page"
        page.config = {"theme": "modern"}
        page.is_published = True
        return page
    
    @pytest.fixture
    def mock_components(self):
        """Mock de componentes"""
        hero_component = Mock(spec=Component)
        hero_component.id = 1
        hero_component.type = "hero"
        hero_component.content = {
            "title": "Welcome",
            "subtitle": "This is amazing",
            "cta_text": "Get Started",
            "cta_link": "/start"
        }
        hero_component.styles = {"backgroundColor": "#f0f0f0"}
        hero_component.position = 1
        hero_component.is_visible = True
        
        text_component = Mock(spec=Component)
        text_component.id = 2
        text_component.type = "text"
        text_component.content = {
            "text": "<p>This is some test content</p>",
            "alignment": "center"
        }
        text_component.styles = {"padding": "40px"}
        text_component.position = 2
        text_component.is_visible = True
        
        return [hero_component, text_component]
    
    def test_dict_to_css(self, generator):
        """Test conversión de diccionario a CSS"""
        styles = {
            "backgroundColor": "#ffffff",
            "fontSize": "16px",
            "marginTop": "20px"
        }
        css = generator._dict_to_css(styles)
        expected = "background-color: #ffffff; font-size: 16px; margin-top: 20px"
        assert css == expected
    
    def test_generate_hero_component(self, generator):
        """Test generación de componente hero"""
        content = {
            "title": "Test Hero",
            "subtitle": "Test subtitle",
            "image": "https://example.com/image.jpg",
            "cta_text": "Click me",
            "cta_link": "/test"
        }
        styles = "background-color: #000000"
        
        html = generator._generate_hero(content, styles)
        
        assert "Test Hero" in html
        assert "Test subtitle" in html
        assert "https://example.com/image.jpg" in html
        assert "Click me" in html
        assert "/test" in html
        assert "background-color: #000000" in html
    
    def test_generate_text_component(self, generator):
        """Test generación de componente texto"""
        content = {
            "text": "<p>Test content</p>",
            "alignment": "center"
        }
        styles = "color: red"
        
        html = generator._generate_text(content, styles)
        
        assert "Test content" in html
        assert "text-align: center" in html
        assert "color: red" in html
    
    def test_generate_image_component(self, generator):
        """Test generación de componente imagen"""
        content = {
            "src": "https://example.com/test.jpg",
            "alt": "Test image",
            "caption": "Test caption"
        }
        styles = "border: 1px solid black"
        
        html = generator._generate_image(content, styles)
        
        assert "https://example.com/test.jpg" in html
        assert "Test image" in html
        assert "Test caption" in html
        assert "border: 1px solid black" in html
    
    def test_generate_button_component(self, generator):
        """Test generación de componente botón"""
        content = {
            "text": "Test Button",
            "link": "/test-link",
            "variant": "primary"
        }
        styles = "margin: 10px"
        
        html = generator._generate_button(content, styles)
        
        assert "Test Button" in html
        assert "/test-link" in html
        assert "background: #007bff" in html  # primary variant
        assert "margin: 10px" in html
    
    def test_generate_header_component(self, generator):
        """Test generación de componente header"""
        content = {
            "title": "Test Site",
            "logo": "https://example.com/logo.png",
            "menu_items": [
                {"text": "Home", "link": "/"},
                {"text": "About", "link": "/about"}
            ]
        }
        styles = "background: white"
        
        html = generator._generate_header(content, styles)
        
        assert "Test Site" in html
        assert "https://example.com/logo.png" in html
        assert "Home" in html
        assert "About" in html
        assert "background: white" in html
    
    def test_generate_footer_component(self, generator):
        """Test generación de componente footer"""
        content = {
            "text": "© 2024 Test Company",
            "links": [
                {"text": "Privacy", "url": "/privacy"},
                {"text": "Terms", "url": "/terms"}
            ]
        }
        styles = "background: gray"
        
        html = generator._generate_footer(content, styles)
        
        assert "© 2024 Test Company" in html
        assert "Privacy" in html
        assert "Terms" in html
        assert "background: gray" in html
    
    def test_generate_unknown_component(self, generator):
        """Test generación de componente desconocido"""
        component = Mock(spec=Component)
        component.type = "unknown"
        component.content = {}
        component.styles = {}
        
        html = generator.generate_component_html(component)
        
        assert "Componente no implementado: unknown" in html
        assert "component-unknown" in html
    
    def test_generate_page(self, generator, mock_page, mock_components):
        """Test generación de página completa"""
        # Mock de la query de componentes
        mock_db = Mock()
        mock_query_result = Mock()
        mock_query_result.filter.return_value.order_by.return_value.all.return_value = mock_components
        mock_db.query.return_value = mock_query_result
        
        html = generator.generate_page(mock_page, mock_db)
        
        assert "Test Page" in html  # título
        assert "A test page" in html  # descripción
        assert "Welcome" in html  # contenido del hero
        assert "This is some test content" in html  # contenido del texto
        assert "linear-gradient" in html  # tema modern
    
    def test_deploy_page(self, generator, mock_page, mock_components, temp_output_dir):
        """Test deployment completo de página"""
        # Mock de la query de componentes
        mock_db = Mock()
        mock_query_result = Mock()
        mock_query_result.filter.return_value.order_by.return_value.all.return_value = mock_components
        mock_db.query.return_value = mock_query_result
        
        result_path = generator.deploy_page(mock_page, mock_db)
        
        # Verificar que se creó el directorio (nueva estructura: subdomain/slug)
        expected_dir = Path(temp_output_dir) / "test" / "test-page"
        assert expected_dir.exists()
        assert expected_dir.is_dir()
        
        # Verificar que se creó el archivo HTML
        html_file = expected_dir / "index.html"
        assert html_file.exists()
        
        # Verificar contenido del archivo
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test Page" in content
            assert "Welcome" in content
        
        # Verificar path retornado
        assert str(expected_dir) == result_path
    
    def test_delete_page(self, generator, temp_output_dir):
        """Test eliminación de página deployada"""
        # Crear directorio de prueba
        page_dir = Path(temp_output_dir) / "test-delete"
        page_dir.mkdir()
        (page_dir / "index.html").write_text("test content")
        
        assert page_dir.exists()
        
        # Eliminar página
        result = generator.delete_page("test-delete")
        
        assert result is True
        assert not page_dir.exists()
    
    def test_delete_nonexistent_page(self, generator):
        """Test eliminación de página que no existe"""
        result = generator.delete_page("nonexistent-page")
        assert result is False
    
    def test_copy_assets(self, generator, temp_output_dir):
        """Test copia de assets"""
        # Crear directorio de assets de prueba
        assets_dir = generator.templates_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / "test.css").write_text("body { color: red; }")
        
        target_dir = Path(temp_output_dir) / "test-assets"
        target_dir.mkdir()
        
        generator._copy_assets(target_dir)
        
        # Verificar que se copiaron los assets
        copied_css = target_dir / "assets" / "test.css"
        assert copied_css.exists()
        assert "body { color: red; }" in copied_css.read_text()
    
    def test_generate_page_with_different_themes(self, generator):
        """Test generación con diferentes temas"""
        themes = ["default", "dark", "modern", "minimal"]
        
        for theme in themes:
            page = Mock(spec=Page)
            page.title = f"Test {theme}"
            page.description = "Test description"
            page.config = {"theme": theme}
            page.slug = f"test-{theme}"
            page.subdomain = "test"
            
            mock_db = Mock()
            mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
            
            html = generator.generate_page(page, mock_db)
            
            assert f"Test {theme}" in html
            
            if theme == "dark":
                assert "background-color: #1a1a1a" in html
            elif theme == "modern":
                assert "linear-gradient" in html
            elif theme == "minimal":
                assert "Georgia" in html


class TestComponentRendering:
    """Tests específicos para renderizado de componentes"""
    
    @pytest.fixture
    def generator(self):
        return SiteGenerator()
    
    def test_hero_without_optional_fields(self, generator):
        """Test hero sin campos opcionales"""
        content = {"title": "Just Title"}
        html = generator._generate_hero(content, "")
        
        assert "Just Title" in html
        assert "img" not in html  # no debería haber imagen
        assert "href" not in html  # no debería haber CTA
    
    def test_button_variants(self, generator):
        """Test diferentes variantes de botón"""
        variants = ["primary", "secondary", "outline"]
        
        for variant in variants:
            content = {"text": "Test", "variant": variant}
            html = generator._generate_button(content, "")
            
            if variant == "primary":
                assert "#007bff" in html
            elif variant == "secondary":
                assert "#6c757d" in html
            elif variant == "outline":
                assert "transparent" in html
    
    def test_component_with_special_characters(self, generator):
        """Test componentes con caracteres especiales"""
        content = {
            "title": "Título con ñ y acentós",
            "text": "<script>alert('xss')</script>"
        }
        
        html = generator._generate_hero(content, "")
        
        assert "Título con ñ y acentós" in html
        # Jinja2 debería escapar el script tag
        assert "&lt;script&gt;" in html or "script" not in html.lower()


class TestErrorHandling:
    """Tests para manejo de errores"""
    
    @pytest.fixture
    def generator(self):
        return SiteGenerator()
    
    def test_component_with_missing_content(self, generator):
        """Test componente con contenido faltante"""
        component = Mock(spec=Component)
        component.type = "hero"
        component.content = {}  # contenido vacío
        component.styles = {}
        
        html = generator.generate_component_html(component)
        
        # No debería fallar, debería usar valores por defecto
        assert "section" in html
        assert "hero" in html
    
    def test_invalid_css_styles(self, generator):
        """Test con estilos CSS inválidos"""
        styles = {
            "invalid-property": "some-value",
            "": "empty-key"
        }
        
        # No debería fallar
        css = generator._dict_to_css(styles)
        assert isinstance(css, str)