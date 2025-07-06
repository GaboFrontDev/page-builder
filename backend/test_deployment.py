import pytest
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import BackgroundTasks

from main import app
from routers.deployment import deploy_page_task
from models import Page, Component
from generator import SiteGenerator
from database import get_db


class TestDeploymentEndpoints:
    
    @pytest.fixture
    def client(self):
        # Override get_db dependency
        def override_get_db():
            return Mock()
        
        app.dependency_overrides[get_db] = override_get_db
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()
    
    @pytest.fixture
    def temp_output_dir(self):
        """Directorio temporal para tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_published_page(self):
        """Mock de página publicada"""
        page = Mock(spec=Page)
        page.id = 1
        page.title = "Published Page"
        page.slug = "published-page"
        page.description = "A published test page"
        page.is_published = True
        page.subdomain = "test"
        return page
    
    @pytest.fixture
    def mock_unpublished_page(self):
        """Mock de página no publicada"""
        page = Mock(spec=Page)
        page.id = 2
        page.title = "Unpublished Page"
        page.slug = "unpublished-page"
        page.description = "An unpublished test page"
        page.is_published = False
        page.subdomain = "test"
        return page
    
    def test_deploy_published_page_success(self, client):
        """Test deployment exitoso de página publicada"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page query
            mock_page = Mock()
            mock_page.id = 1
            mock_page.slug = "test-page"
            mock_page.is_published = True
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Deployment started"
            assert data["page_id"] == 1
            assert data["slug"] == "test-page"
            assert data["url"] == "http://test-page.localhost"
    
    def test_deploy_unpublished_page_fails(self, client):
        """Test que falla deployment de página no publicada"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock unpublished page
            mock_page = Mock()
            mock_page.id = 2
            mock_page.is_published = False
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/2")
            
            assert response.status_code == 400
            assert "must be published" in response.json()["detail"]
    
    def test_deploy_nonexistent_page_fails(self, client):
        """Test que falla deployment de página inexistente"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock no page found
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            response = client.post("/api/deploy/999")
            
            assert response.status_code == 404
            assert "Page not found" in response.json()["detail"]
    
    def test_deploy_by_slug_success(self, client):
        """Test deployment por slug"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page query by slug
            mock_page = Mock()
            mock_page.slug = "test-slug"
            mock_page.is_published = True
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            response = client.post("/api/deploy/slug/test-slug")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Deployment started"
            assert data["slug"] == "test-slug"
            assert data["url"] == "http://test-slug.localhost"
    
    def test_undeploy_page_success(self, client):
        """Test undeploy exitoso"""
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator.delete_page') as mock_delete:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page
            mock_page = Mock()
            mock_page.id = 1
            mock_page.slug = "test-page"
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            # Mock successful deletion
            mock_delete.return_value = True
            
            response = client.delete("/api/deploy/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Page undeployed successfully"
            assert data["slug"] == "test-page"
    
    def test_undeploy_page_not_deployed(self, client):
        """Test undeploy de página no deployada"""
        with patch('routers.deployment.get_db') as mock_get_db, \
             patch('routers.deployment.generator.delete_page') as mock_delete:
            
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page
            mock_page = Mock()
            mock_page.id = 1
            mock_page.slug = "test-page"
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            # Mock deletion returns False (not deployed)
            mock_delete.return_value = False
            
            response = client.delete("/api/deploy/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Page was not deployed"
    
    def test_undeploy_by_slug(self, client):
        """Test undeploy por slug"""
        with patch('routers.deployment.generator.delete_page') as mock_delete:
            mock_delete.return_value = True
            
            response = client.delete("/api/deploy/slug/test-slug")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Page undeployed successfully"
            assert data["slug"] == "test-slug"
    
    @patch('os.path.exists')
    def test_deployment_status_deployed(self, mock_exists, client):
        """Test status de página deployada"""
        # Mock que existe el directorio y archivo
        mock_exists.side_effect = lambda path: True
        
        response = client.get("/api/deploy/status/test-page")
        
        assert response.status_code == 200
        data = response.json()
        assert data["deployed"] is True
        assert data["slug"] == "test-page"
        assert data["url"] == "http://test-page.localhost"
        assert data["path"] == "/var/www/sites/test-page"
    
    @patch('os.path.exists')
    def test_deployment_status_not_deployed(self, mock_exists, client):
        """Test status de página no deployada"""
        # Mock que no existe
        mock_exists.return_value = False
        
        response = client.get("/api/deploy/status/test-page")
        
        assert response.status_code == 200
        data = response.json()
        assert data["deployed"] is False
        assert data["slug"] == "test-page"
        assert "url" not in data
    
    def test_rebuild_all_sites(self, client):
        """Test rebuild de todos los sitios"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock published pages
            mock_page1 = Mock()
            mock_page1.id = 1
            mock_page1.slug = "page-1"
            mock_page1.subdomain = "test"
            mock_page2 = Mock()
            mock_page2.id = 2
            mock_page2.slug = "page-2"
            mock_page2.subdomain = "test"
            
            mock_db.query.return_value.filter.return_value.all.return_value = [mock_page1, mock_page2]
            
            response = client.post("/api/deploy/rebuild-all")
            
            assert response.status_code == 200
            data = response.json()
            assert "Rebuild started for 2 pages" in data["message"]
            assert len(data["pages"]) == 2
    
    def test_rebuild_all_no_pages(self, client):
        """Test rebuild cuando no hay páginas"""
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock no published pages
            mock_db.query.return_value.filter.return_value.all.return_value = []
            
            response = client.post("/api/deploy/rebuild-all")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "No published pages found"
    
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_list_deployed_sites(self, mock_isdir, mock_exists, mock_listdir, client):
        """Test listado de sitios deployados"""
        # Mock directory structure
        mock_listdir.return_value = ["site1", "site2", "not-a-site"]
        mock_isdir.side_effect = lambda path: "not-a-site" not in path
        mock_exists.side_effect = lambda path: "index.html" in path and "not-a-site" not in path
        
        response = client.get("/api/deploy/list")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["deployed_sites"]) == 2
        assert data["deployed_sites"][0]["slug"] == "site1"
        assert data["deployed_sites"][1]["slug"] == "site2"
    
    @patch('os.path.exists')
    def test_list_deployed_sites_no_directory(self, mock_exists, client):
        """Test listado cuando no existe el directorio"""
        mock_exists.return_value = False
        
        response = client.get("/api/deploy/list")
        
        assert response.status_code == 200
        data = response.json()
        assert data["deployed_sites"] == []


class TestBackgroundDeploymentTask:
    """Tests para la tarea background de deployment"""
    
    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_page_with_components(self):
        """Mock de página con componentes"""
        page = Mock(spec=Page)
        page.id = 1
        page.title = "Test Page"
        page.slug = "test-page"
        page.description = "Test description"
        page.config = {"theme": "default"}
        page.subdomain = "test"
        
        # Mock components
        component = Mock(spec=Component)
        component.id = 1
        component.type = "hero"
        component.content = {"title": "Welcome"}
        component.styles = {}
        component.position = 1
        component.is_visible = True
        component.page_id = 1
        
        return page, [component]
    
    @patch('routers.deployment.SessionLocal')
    @patch('routers.deployment.generator')
    def test_deploy_page_task_success(self, mock_generator, mock_session_local, mock_page_with_components):
        """Test tarea background exitosa"""
        page, components = mock_page_with_components
        
        # Mock database session
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = page
        
        # Mock generator
        mock_generator.deploy_page.return_value = "/var/www/sites/test-page"
        
        # Execute task
        deploy_page_task(page, mock_db)
        
        # Verify calls
        mock_generator.deploy_page.assert_called_once_with(page, mock_db)
        mock_db.close.assert_called_once()
    
    @patch('routers.deployment.SessionLocal')
    def test_deploy_page_task_page_not_found(self, mock_session_local, mock_page_with_components):
        """Test tarea cuando la página no existe"""
        page, components = mock_page_with_components
        
        # Mock database session
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Should not raise exception
        deploy_page_task(page, mock_db)
        
        mock_db.close.assert_called_once()
    
    @patch('routers.deployment.SessionLocal')
    @patch('routers.deployment.generator')
    def test_deploy_page_task_generator_error(self, mock_generator, mock_session_local, mock_page_with_components):
        """Test tarea cuando el generador falla"""
        page, components = mock_page_with_components
        
        # Mock database session
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = page
        
        # Mock generator to raise exception
        mock_generator.deploy_page.side_effect = Exception("Generator error")
        
        # Should raise exception
        with pytest.raises(Exception, match="Generator error"):
            deploy_page_task(page, mock_db)
        
        mock_db.close.assert_called_once()


class TestDeploymentIntegration:
    """Tests de integración para deployment"""
    
    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @patch('routers.deployment.generator')
    def test_full_deployment_workflow(self, mock_generator, temp_output_dir):
        """Test workflow completo de deployment"""
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Setup mock generator
        mock_generator.deploy_page.return_value = f"{temp_output_dir}/test-page"
        mock_generator.delete_page.return_value = True
        
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page
            mock_page = Mock()
            mock_page.id = 1
            mock_page.slug = "test-page"
            mock_page.is_published = True
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            # 1. Deploy page
            response = client.post("/api/deploy/1")
            assert response.status_code == 200
            
            # 2. Check status (mock as deployed)
            with patch('os.path.exists', return_value=True):
                response = client.get("/api/deploy/status/test-page")
                assert response.status_code == 200
                assert response.json()["deployed"] is True
            
            # 3. Undeploy page
            response = client.delete("/api/deploy/1")
            assert response.status_code == 200
            
            # 4. Check status (mock as not deployed)
            with patch('os.path.exists', return_value=False):
                response = client.get("/api/deploy/status/test-page")
                assert response.status_code == 200
                assert response.json()["deployed"] is False


class TestDeploymentErrorHandling:
    """Tests para manejo de errores en deployment"""
    
    def test_deployment_with_database_error(self):
        """Test deployment cuando hay error de base de datos"""
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        with patch('routers.deployment.get_db') as mock_get_db:
            # Mock database error
            mock_get_db.side_effect = Exception("Database connection error")
            
            response = client.post("/api/deploy/1")
            
            # Should handle the error gracefully
            assert response.status_code == 500
    
    @patch('routers.deployment.generator')
    def test_deployment_with_generator_error(self, mock_generator):
        """Test deployment cuando el generador falla"""
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        with patch('routers.deployment.get_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock page
            mock_page = Mock()
            mock_page.id = 1
            mock_page.is_published = True
            mock_page.subdomain = "test"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_page
            
            # Mock generator error in background task
            mock_generator.deploy_page.side_effect = Exception("Generator failed")
            
            # Should still return 200 since it's a background task
            response = client.post("/api/deploy/1")
            assert response.status_code == 200