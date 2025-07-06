import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from generator import SiteGenerator
from models import Page, Component


class TestTemplateSystem:
    """Tests para el sistema de templates"""
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def generator_with_custom_templates(self, temp_dir):
        """Generator con directorio de templates personalizado"""
        templates_dir = Path(temp_dir) / "templates"
        templates_dir.mkdir()
        
        # Crear template base personalizado
        base_template = templates_dir / "base.html"
        base_template.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    {% if theme == 'custom' %}
    <style>body { background: purple; }</style>
    {% endif %}
</head>
<body>
    {{ content|safe }}
</body>
</html>
        """.strip())
        
        # Crear directorio de assets
        assets_dir = templates_dir / "assets"
        assets_dir.mkdir()
        (assets_dir / "custom.css").write_text("/* Custom CSS */")
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = templates_dir
        
        # Reconfigurar Jinja2 con nuevo directorio
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        generator.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        return generator
    
    def test_base_template_rendering(self, generator_with_custom_templates):
        """Test renderizado del template base"""
        generator = generator_with_custom_templates
        
        # Mock page
        page = Mock(spec=Page)
        page.title = "Test Template Page"
        page.description = "Testing templates"
        page.config = {"theme": "custom"}
        page.slug = "test-template"
        page.subdomain = "test"
        
        # Mock empty components
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        assert "Test Template Page" in html
        assert "Testing templates" in html
        assert "background: purple" in html  # custom theme
    
    def test_theme_variations(self, generator_with_custom_templates):
        """Test diferentes variaciones de tema"""
        generator = generator_with_custom_templates
        themes = ["default", "dark", "modern", "minimal", "custom"]
        
        for theme in themes:
            page = Mock(spec=Page)
            page.title = f"Test {theme.title()} Theme"
            page.description = f"Testing {theme} theme"
            page.config = {"theme": theme}
            page.slug = f"test-{theme}"
            page.subdomain = "test"
            
            mock_db = Mock()
            mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
            
            html = generator.generate_page(page, mock_db)
            
            assert f"Test {theme.title()} Theme" in html
            
            if theme == "custom":
                assert "background: purple" in html
    
    def test_template_with_missing_variables(self, generator_with_custom_templates):
        """Test template cuando faltan variables"""
        generator = generator_with_custom_templates
        
        page = Mock(spec=Page)
        page.title = None  # Variable faltante
        page.description = "Test description"
        page.config = {}
        page.slug = "test-missing"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # No debería fallar
        html = generator.generate_page(page, mock_db)
        assert "Test description" in html


class TestThemeSystem:
    """Tests específicos para el sistema de temas"""
    
    @pytest.fixture
    def generator(self):
        return SiteGenerator()
    
    def test_default_theme(self, generator):
        """Test tema por defecto"""
        page = Mock(spec=Page)
        page.title = "Default Theme Test"
        page.description = "Testing default theme"
        page.config = {"theme": "default"}
        page.slug = "default-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar estilos del tema default
        assert "font-family: -apple-system" in html
        assert "background-color: #fff" in html
        assert "color: #333" in html
    
    def test_dark_theme(self, generator):
        """Test tema oscuro"""
        page = Mock(spec=Page)
        page.title = "Dark Theme Test"
        page.description = "Testing dark theme"
        page.config = {"theme": "dark"}
        page.slug = "dark-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar estilos del tema dark
        assert "background-color: #1a1a1a" in html
        assert "color: #fff" in html
    
    def test_modern_theme(self, generator):
        """Test tema moderno"""
        page = Mock(spec=Page)
        page.title = "Modern Theme Test"
        page.description = "Testing modern theme"
        page.config = {"theme": "modern"}
        page.slug = "modern-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar estilos del tema modern
        assert "linear-gradient" in html
        assert "backdrop-filter: blur" in html
        assert "rgba(255,255,255,0.1)" in html
    
    def test_minimal_theme(self, generator):
        """Test tema minimal"""
        page = Mock(spec=Page)
        page.title = "Minimal Theme Test"
        page.description = "Testing minimal theme"
        page.config = {"theme": "minimal"}
        page.slug = "minimal-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar estilos del tema minimal
        assert "Georgia" in html
        assert "background-color: #fafafa" in html
    
    def test_unknown_theme_fallback(self, generator):
        """Test fallback para tema desconocido"""
        page = Mock(spec=Page)
        page.title = "Unknown Theme Test"
        page.description = "Testing unknown theme"
        page.config = {"theme": "nonexistent"}
        page.slug = "unknown-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Debería usar el tema por defecto
        assert "Unknown Theme Test" in html
        assert "<!DOCTYPE html>" in html
    
    def test_theme_without_config(self, generator):
        """Test página sin configuración de tema"""
        page = Mock(spec=Page)
        page.title = "No Theme Test"
        page.description = "Testing no theme"
        page.config = {}  # Sin tema
        page.slug = "no-theme-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Debería usar el tema por defecto
        assert "No Theme Test" in html
        assert "font-family: -apple-system" in html


class TestResponsiveDesign:
    """Tests para diseño responsivo"""
    
    @pytest.fixture
    def generator(self):
        return SiteGenerator()
    
    def test_responsive_css_included(self, generator):
        """Test que se incluye CSS responsivo"""
        page = Mock(spec=Page)
        page.title = "Responsive Test"
        page.description = "Testing responsive design"
        page.config = {"theme": "default"}
        page.slug = "responsive-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar media queries
        assert "@media (max-width: 768px)" in html
        assert "font-size: 2rem !important" in html
        assert "padding: 0 15px" in html
    
    def test_mobile_optimization(self, generator):
        """Test optimizaciones para móvil"""
        page = Mock(spec=Page)
        page.title = "Mobile Test"
        page.description = "Testing mobile optimization"
        page.config = {"theme": "default"}
        page.slug = "mobile-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        html = generator.generate_page(page, mock_db)
        
        # Verificar viewport meta tag
        assert 'name="viewport"' in html
        assert "width=device-width" in html
        assert "initial-scale=1.0" in html


class TestAssetManagement:
    """Tests para gestión de assets"""
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def generator_with_assets(self, temp_dir):
        """Generator con assets de prueba"""
        templates_dir = Path(temp_dir) / "templates"
        templates_dir.mkdir()
        
        # Crear directorio de assets con archivos
        assets_dir = templates_dir / "assets"
        assets_dir.mkdir()
        
        # CSS personalizado
        (assets_dir / "custom.css").write_text("""
        .custom-style {
            color: blue;
            font-size: 18px;
        }
        """)
        
        # JavaScript
        (assets_dir / "script.js").write_text("""
        console.log('Custom script loaded');
        """)
        
        # Imagen de prueba (contenido dummy)
        (assets_dir / "logo.png").write_bytes(b"dummy image data")
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = templates_dir
        
        return generator
    
    def test_assets_copied_during_deployment(self, generator_with_assets, temp_dir):
        """Test que los assets se copian durante el deployment"""
        generator = generator_with_assets
        
        page = Mock(spec=Page)
        page.title = "Assets Test"
        page.description = "Testing asset copying"
        page.config = {"theme": "default"}
        page.slug = "assets-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Deploy page
        result_path = generator.deploy_page(page, mock_db)
        
        # Verificar que se crearon los assets
        assets_path = Path(result_path) / "assets"
        assert assets_path.exists()
        assert (assets_path / "custom.css").exists()
        assert (assets_path / "script.js").exists()
        assert (assets_path / "logo.png").exists()
        
        # Verificar contenido
        css_content = (assets_path / "custom.css").read_text()
        assert "custom-style" in css_content
        assert "color: blue" in css_content
    
    def test_assets_not_copied_without_source(self, temp_dir):
        """Test que no se copian assets si no existen en la fuente"""
        generator = SiteGenerator(output_dir=temp_dir)
        
        page = Mock(spec=Page)
        page.title = "No Assets Test"
        page.description = "Testing without assets"
        page.config = {"theme": "default"}
        page.slug = "no-assets-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Deploy page
        result_path = generator.deploy_page(page, mock_db)
        
        # Verificar que no se crearon assets
        assets_path = Path(result_path) / "assets"
        assert not assets_path.exists()


class TestTemplateErrorHandling:
    """Tests para manejo de errores en templates"""
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_missing_template_file(self, temp_dir):
        """Test cuando falta el archivo de template"""
        empty_templates_dir = Path(temp_dir) / "empty_templates"
        empty_templates_dir.mkdir()
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = empty_templates_dir
        
        # Reconfigurar Jinja2 con directorio vacío
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        generator.env = Environment(
            loader=FileSystemLoader(str(empty_templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        page = Mock(spec=Page)
        page.title = "Missing Template Test"
        page.description = "Testing missing template"
        page.config = {"theme": "default"}
        page.slug = "missing-template-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Debería lanzar excepción
        with pytest.raises(Exception):
            generator.generate_page(page, mock_db)
    
    def test_invalid_template_syntax(self, temp_dir):
        """Test template con sintaxis inválida"""
        templates_dir = Path(temp_dir) / "templates"
        templates_dir.mkdir()
        
        # Crear template con sintaxis inválida
        base_template = templates_dir / "base.html"
        base_template.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    {% invalid_syntax %}
</head>
<body>
    {{ content|safe }}
</body>
</html>
        """.strip())
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = templates_dir
        
        # Reconfigurar Jinja2
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        generator.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        page = Mock(spec=Page)
        page.title = "Invalid Syntax Test"
        page.description = "Testing invalid template syntax"
        page.config = {"theme": "default"}
        page.slug = "invalid-syntax-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Debería lanzar excepción de Jinja2
        with pytest.raises(Exception):
            generator.generate_page(page, mock_db)


class TestTemplateCustomization:
    """Tests para personalización de templates"""
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_custom_template_variables(self, temp_dir):
        """Test template con variables personalizadas"""
        templates_dir = Path(temp_dir) / "templates"
        templates_dir.mkdir()
        
        # Template con variables extra
        base_template = templates_dir / "base.html"
        base_template.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta name="author" content="{{ author or 'Unknown' }}">
    <meta name="keywords" content="{{ keywords or '' }}">
</head>
<body class="{{ body_class or 'default' }}">
    {{ content|safe }}
</body>
</html>
        """.strip())
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = templates_dir
        
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        generator.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        page = Mock(spec=Page)
        page.title = "Custom Variables Test"
        page.description = "Testing custom template variables"
        page.config = {
            "theme": "default",
            "author": "Test Author",
            "keywords": "test, template, custom",
            "body_class": "custom-page"
        }
        page.slug = "custom-vars-test"
        page.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Override template.render para pasar variables extra
        original_render = generator.env.get_template("base.html").render
        
        def custom_render(**kwargs):
            # Agregar variables del config
            extra_vars = page.config.copy()
            extra_vars.update(kwargs)
            return original_render(**extra_vars)
        
        with patch.object(generator.env.get_template("base.html"), 'render', custom_render):
            html = generator.generate_page(page, mock_db)
        
        assert "Custom Variables Test" in html
        assert 'content="Test Author"' in html
        assert 'content="test, template, custom"' in html
        assert 'class="custom-page"' in html
    
    def test_conditional_template_sections(self, temp_dir):
        """Test secciones condicionales en template"""
        templates_dir = Path(temp_dir) / "templates"
        templates_dir.mkdir()
        
        # Template con lógica condicional
        base_template = templates_dir / "base.html"
        base_template.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    {% if analytics_id %}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ analytics_id }}"></script>
    {% endif %}
</head>
<body>
    {% if show_header %}
    <header>Header Content</header>
    {% endif %}
    
    {{ content|safe }}
    
    {% if show_footer %}
    <footer>Footer Content</footer>
    {% endif %}
</body>
</html>
        """.strip())
        
        generator = SiteGenerator(output_dir=temp_dir)
        generator.templates_dir = templates_dir
        
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        generator.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Test con header y footer habilitados
        page1 = Mock(spec=Page)
        page1.title = "With Header Footer"
        page1.description = "Testing with header and footer"
        page1.config = {
            "theme": "default",
            "show_header": True,
            "show_footer": True,
            "analytics_id": "GA_TRACKING_ID"
        }
        page1.slug = "with-header-footer"
        page1.subdomain = "test"
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Mock custom render como antes
        original_render = generator.env.get_template("base.html").render
        
        def custom_render(**kwargs):
            extra_vars = page1.config.copy()
            extra_vars.update(kwargs)
            return original_render(**extra_vars)
        
        with patch.object(generator.env.get_template("base.html"), 'render', custom_render):
            html1 = generator.generate_page(page1, mock_db)
        
        assert "Header Content" in html1
        assert "Footer Content" in html1
        assert "GA_TRACKING_ID" in html1
        
        # Test sin header ni footer
        page2 = Mock(spec=Page)
        page2.title = "Without Header Footer"
        page2.description = "Testing without header and footer"
        page2.config = {
            "theme": "default",
            "show_header": False,
            "show_footer": False
        }
        page2.slug = "without-header-footer"
        page2.subdomain = "test"
        
        def custom_render2(**kwargs):
            extra_vars = page2.config.copy()
            extra_vars.update(kwargs)
            return original_render(**extra_vars)
        
        with patch.object(generator.env.get_template("base.html"), 'render', custom_render2):
            html2 = generator.generate_page(page2, mock_db)
        
        assert "Header Content" not in html2
        assert "Footer Content" not in html2
        assert "googletagmanager" not in html2