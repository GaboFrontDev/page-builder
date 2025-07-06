import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from main import app
from generator import SiteGenerator


class TestFullIntegration:
    """Tests de integración completa del sistema"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_complete_page_creation_and_deployment_workflow(self, client, temp_output_dir):
        """Test del workflow completo: crear página, agregar componentes, deployar"""
        
        # Step 1: Crear página
        page_data = {
            "title": "Integration Test Page",
            "slug": "integration-test",
            "description": "A complete integration test",
            "config": {"theme": "modern"},
            "is_published": True
        }
        
        with patch('routers.pages.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock que no existe página con mismo slug
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            # Mock creación de página
            mock_page = Mock()
            mock_page.id = 1
            mock_page.title = page_data["title"]
            mock_page.slug = page_data["slug"]
            mock_page.description = page_data["description"]
            mock_page.config = page_data["config"]
            mock_page.is_published = page_data["is_published"]
            mock_page.owner_id = None
            mock_page.created_at = "2024-01-01T00:00:00"
            mock_page.updated_at = "2024-01-01T00:00:00"
            mock_page.components = []
            
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', 1))
            
            response = client.post("/api/pages/", json=page_data)
            assert response.status_code == 200
            
            page_response = response.json()
            page_id = page_response["id"] if "id" in page_response else 1
        
        # Step 2: Agregar componente hero
        hero_component = {
            "type": "hero",
            "content": {
                "title": "Welcome to Integration Test",
                "subtitle": "This page was created through integration testing",
                "cta_text": "Get Started",
                "cta_link": "/start"
            },
            "styles": {"backgroundColor": "#667eea"},
            "position": 1,
            "is_visible": True
        }
        
        with patch('routers.components.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock component creation
            mock_component = Mock()
            mock_component.id = 1
            mock_component.type = hero_component["type"]
            mock_component.content = hero_component["content"]
            mock_component.styles = hero_component["styles"]
            mock_component.position = hero_component["position"]
            mock_component.is_visible = hero_component["is_visible"]
            mock_component.page_id = page_id
            mock_component.created_at = "2024-01-01T00:00:00"
            
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', 1))
            
            response = client.post(f"/api/components/?page_id={page_id}", json=hero_component)
            assert response.status_code == 200
        
        # Step 3: Agregar componente texto
        text_component = {
            "type": "text",
            "content": {
                "text": "<p>This is the main content of our integration test page. It demonstrates the complete workflow.</p>",
                "alignment": "center"
            },
            "styles": {"padding": "40px", "color": "#333"},
            "position": 2,
            "is_visible": True
        }
        
        with patch('routers.components.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_component2 = Mock()
            mock_component2.id = 2
            mock_component2.type = text_component["type"]
            mock_component2.content = text_component["content"]
            mock_component2.styles = text_component["styles"]
            mock_component2.position = text_component["position"]
            mock_component2.is_visible = text_component["is_visible"]
            mock_component2.page_id = page_id
            mock_component2.created_at = "2024-01-01T00:00:00"
            
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', 2))
            
            response = client.post(f"/api/components/?page_id={page_id}", json=text_component)
            assert response.status_code == 200
        
        # Step 4: Deployar página
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator') as mock_generator:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock página para deployment
            mock_deploy_page = Mock()
            mock_deploy_page.id = page_id
            mock_deploy_page.slug = "integration-test"
            mock_deploy_page.is_published = True
            mock_db.query.return_value.filter.return_value.first.return_value = mock_deploy_page
            
            # Mock generator success
            mock_generator.deploy_page.return_value = f"{temp_output_dir}/integration-test"
            
            response = client.post(f"/api/deploy/{page_id}")
            assert response.status_code == 200
            
            deploy_response = response.json()
            assert deploy_response["message"] == "Deployment started"
            assert deploy_response["slug"] == "integration-test"
            assert deploy_response["url"] == "http://integration-test.localhost"
        
        # Step 5: Verificar status del deployment
        with patch('os.path.exists', return_value=True):
            response = client.get("/api/deploy/status/integration-test")
            assert response.status_code == 200
            
            status_response = response.json()
            assert status_response["deployed"] is True
            assert status_response["slug"] == "integration-test"
    
    def test_page_update_and_redeploy_workflow(self, client):
        """Test actualización de página y re-deployment"""
        
        page_id = 1
        
        # Step 1: Actualizar página
        update_data = {
            "title": "Updated Integration Test Page",
            "config": {"theme": "dark"}
        }
        
        with patch('routers.pages.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock página existente
            mock_page = Mock()
            mock_page.id = page_id
            mock_page.title = "Integration Test Page"
            mock_page.slug = "integration-test"
            mock_page.description = "A complete integration test"
            mock_page.config = {"theme": "modern"}
            mock_page.is_published = True
            
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            mock_db.commit = Mock()
            mock_db.refresh = Mock()
            
            response = client.put(f"/api/pages/{page_id}", json=update_data)
            assert response.status_code == 200
        
        # Step 2: Re-deployar
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator') as mock_generator:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_page.title = "Updated Integration Test Page"  # Reflect update
            mock_page.config = {"theme": "dark"}
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post(f"/api/deploy/{page_id}")
            assert response.status_code == 200
    
    def test_component_reordering_and_redeploy(self, client):
        """Test reordenamiento de componentes y re-deployment"""
        
        component_id = 1
        new_position = 3
        
        with patch('routers.components.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock component
            mock_component = Mock()
            mock_component.id = component_id
            mock_component.position = 1
            mock_component.page_id = 1
            
            mock_db.query.return_value.filter.return_value.first.return_value = mock_component
            mock_db.commit = Mock()
            mock_db.refresh = Mock()
            
            response = client.post(f"/api/components/{component_id}/reorder", json={"new_position": new_position})
            assert response.status_code == 200
    
    def test_error_recovery_workflow(self, client):
        """Test recuperación de errores en el workflow"""
        
        # Test 1: Intentar deployar página no publicada
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_page = Mock()
            mock_page.is_published = False
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/1")
            assert response.status_code == 400
            assert "must be published" in response.json()["detail"]
        
        # Test 2: Publicar página y deployar exitosamente
        with patch('routers.pages.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_page = Mock()
            mock_page.id = 1
            mock_page.is_published = False
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            mock_db.commit = Mock()
            mock_db.refresh = Mock()
            
            response = client.post("/api/pages/1/publish")
            assert response.status_code == 200
        
        # Test 3: Ahora deployar exitosamente
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator') as mock_generator:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_page.is_published = True  # Now published
            mock_page.slug = "test-page"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/1")
            assert response.status_code == 200


class TestRealWorldScenarios:
    """Tests de escenarios del mundo real"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_complex_landing_page_creation(self, client):
        """Test creación de landing page compleja"""
        
        # Crear página para empresa de tecnología
        page_data = {
            "title": "TechCorp - Soluciones Innovadoras",
            "slug": "techcorp-landing",
            "description": "Descubre nuestras soluciones tecnológicas de vanguardia",
            "config": {"theme": "modern"},
            "is_published": True
        }
        
        with patch('routers.pages.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            mock_page = Mock()
            mock_page.id = 1
            for key, value in page_data.items():
                setattr(mock_page, key, value)
            mock_page.owner_id = None
            mock_page.created_at = "2024-01-01T00:00:00"
            mock_page.updated_at = "2024-01-01T00:00:00"
            mock_page.components = []
            
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', 1))
            
            response = client.post("/api/pages/", json=page_data)
            assert response.status_code == 200
        
        # Componentes de la landing page
        components = [
            {
                "type": "header",
                "content": {
                    "title": "TechCorp",
                    "logo": "https://techcorp.com/logo.png",
                    "menu_items": [
                        {"text": "Inicio", "link": "/"},
                        {"text": "Servicios", "link": "/servicios"},
                        {"text": "Contacto", "link": "/contacto"}
                    ]
                },
                "styles": {"backgroundColor": "#ffffff", "borderBottom": "1px solid #eee"},
                "position": 1
            },
            {
                "type": "hero",
                "content": {
                    "title": "Transformamos tu negocio con tecnología",
                    "subtitle": "Soluciones innovadoras para empresas del futuro",
                    "cta_text": "Conocer más",
                    "cta_link": "/servicios",
                    "image": "https://techcorp.com/hero.jpg"
                },
                "styles": {"minHeight": "80vh"},
                "position": 2
            },
            {
                "type": "text",
                "content": {
                    "text": "<h2>Nuestros Servicios</h2><p>Ofrecemos una gama completa de servicios tecnológicos.</p>",
                    "alignment": "center"
                },
                "styles": {"padding": "80px 20px"},
                "position": 3
            },
            {
                "type": "footer",
                "content": {
                    "text": "© 2024 TechCorp. Todos los derechos reservados.",
                    "links": [
                        {"text": "Privacidad", "url": "/privacidad"},
                        {"text": "Términos", "url": "/terminos"}
                    ]
                },
                "styles": {"backgroundColor": "#333", "color": "#fff"},
                "position": 4
            }
        ]
        
        # Agregar cada componente
        for i, component in enumerate(components):
            component["is_visible"] = True
            
            with patch('routers.components.get_db') as mock_get_db:
                mock_db = Mock()
                mock_get_db.return_value = mock_db
                
                mock_component = Mock()
                mock_component.id = i + 1
                for key, value in component.items():
                    setattr(mock_component, key, value)
                mock_component.page_id = 1
                mock_component.created_at = "2024-01-01T00:00:00"
                
                mock_db.add = Mock()
                mock_db.commit = Mock()
                mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', i + 1))
                
                response = client.post("/api/components/?page_id=1", json=component)
                assert response.status_code == 200
        
        # Deployar la página completa
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator') as mock_generator:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            mock_page = Mock()
            mock_page.id = 1
            mock_page.slug = "techcorp-landing"
            mock_page.is_published = True
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/1")
            assert response.status_code == 200
            
            deploy_response = response.json()
            assert deploy_response["url"] == "http://techcorp-landing.localhost"
    
    def test_multiple_sites_management(self, client):
        """Test gestión de múltiples sitios"""
        
        # Crear 3 sitios diferentes
        sites = [
            {"title": "Site A", "slug": "site-a", "theme": "default"},
            {"title": "Site B", "slug": "site-b", "theme": "dark"},
            {"title": "Site C", "slug": "site-c", "theme": "modern"}
        ]
        
        created_sites = []
        
        for i, site in enumerate(sites):
            page_data = {
                "title": site["title"],
                "slug": site["slug"],
                "description": f"Description for {site['title']}",
                "config": {"theme": site["theme"]},
                "is_published": True
            }
            
            with patch('routers.pages.get_db') as mock_get_db:
                mock_db = Mock()
                mock_get_db.return_value = mock_db
                mock_db.query.return_value.filter.return_value.first.return_value = None
                
                mock_page = Mock()
                mock_page.id = i + 1
                for key, value in page_data.items():
                    setattr(mock_page, key, value)
                mock_page.owner_id = None
                mock_page.created_at = "2024-01-01T00:00:00"
                mock_page.updated_at = "2024-01-01T00:00:00"
                mock_page.components = []
                
                mock_db.add = Mock()
                mock_db.commit = Mock()
                mock_db.refresh = Mock(side_effect=lambda x: setattr(x, 'id', i + 1))
                
                response = client.post("/api/pages/", json=page_data)
                assert response.status_code == 200
                created_sites.append(response.json())
        
        # Deployar todos los sitios
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator') as mock_generator:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock all published pages
            mock_pages = []
            for i, site in enumerate(sites):
                mock_page = Mock()
                mock_page.id = i + 1
                mock_page.slug = site["slug"]
                mock_pages.append(mock_page)
            
            mock_db.query.return_value.filter.return_value.all.return_value = mock_pages
            
            response = client.post("/api/deploy/rebuild-all")
            assert response.status_code == 200
            
            rebuild_response = response.json()
            assert "3 pages" in rebuild_response["message"]
            assert len(rebuild_response["pages"]) == 3
        
        # Listar sitios deployados
        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=["site-a", "site-b", "site-c"]), \
             patch('os.path.isdir', return_value=True):
            
            response = client.get("/api/deploy/list")
            assert response.status_code == 200
            
            list_response = response.json()
            assert len(list_response["deployed_sites"]) == 3
            
            deployed_slugs = [site["slug"] for site in list_response["deployed_sites"]]
            assert "site-a" in deployed_slugs
            assert "site-b" in deployed_slugs
            assert "site-c" in deployed_slugs