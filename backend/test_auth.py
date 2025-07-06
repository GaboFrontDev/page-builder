import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import Mock, patch

from main import app
from database import get_db
from models import Base, User
from auth import auth_manager

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAuthManager:
    """Tests para el manager de autenticación"""
    
    def test_password_hashing(self):
        """Test hashing y verificación de contraseñas"""
        password = "testpassword123"
        hashed = auth_manager.get_password_hash(password)
        
        assert hashed != password
        assert auth_manager.verify_password(password, hashed)
        assert not auth_manager.verify_password("wrongpassword", hashed)
    
    def test_create_access_token(self):
        """Test creación de tokens JWT"""
        data = {"sub": "test@example.com"}
        token = auth_manager.create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Test verificación de token válido"""
        data = {"sub": "test@example.com"}
        token = auth_manager.create_access_token(data)
        
        decoded = auth_manager.verify_token(token)
        
        assert decoded is not None
        assert decoded["email"] == "test@example.com"
        assert "exp" in decoded
    
    def test_verify_token_invalid(self):
        """Test verificación de token inválido"""
        invalid_token = "invalid.token.here"
        decoded = auth_manager.verify_token(invalid_token)
        
        assert decoded is None
    
    def test_authenticate_user_success(self):
        """Test autenticación exitosa de usuario"""
        # Setup database with test user
        db = TestingSessionLocal()
        
        # Limpiar usuarios existentes
        db.query(User).delete()
        db.commit()
        
        # Crear usuario de prueba
        hashed_password = auth_manager.get_password_hash("testpass")
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(test_user)
        db.commit()
        
        # Probar autenticación
        authenticated_user = auth_manager.authenticate_user(
            db, "test@example.com", "testpass"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.email == "test@example.com"
        
        db.close()
    
    def test_authenticate_user_wrong_password(self):
        """Test autenticación con contraseña incorrecta"""
        db = TestingSessionLocal()
        
        authenticated_user = auth_manager.authenticate_user(
            db, "test@example.com", "wrongpassword"
        )
        
        assert authenticated_user is None
        db.close()
    
    def test_authenticate_user_not_found(self):
        """Test autenticación con usuario inexistente"""
        db = TestingSessionLocal()
        
        authenticated_user = auth_manager.authenticate_user(
            db, "nonexistent@example.com", "anypassword"
        )
        
        assert authenticated_user is None
        db.close()


class TestAuthEndpoints:
    """Tests para los endpoints de autenticación"""
    
    def setup_method(self):
        """Limpiar base de datos antes de cada test"""
        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()
    
    def test_register_user_success(self):
        """Test registro exitoso de usuario"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["is_active"] == True
        assert "id" in data
        assert "created_at" in data
    
    def test_register_user_duplicate_email(self):
        """Test registro con email duplicado"""
        user_data = {
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123"
        }
        
        # Primer registro
        response1 = client.post("/api/auth/register", json=user_data)
        assert response1.status_code == 200
        
        # Segundo registro con mismo email
        user_data["username"] = "user2"
        response2 = client.post("/api/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]
    
    def test_register_user_duplicate_username(self):
        """Test registro con username duplicado"""
        user_data1 = {
            "email": "user1@example.com",
            "username": "duplicateuser",
            "password": "password123"
        }
        
        user_data2 = {
            "email": "user2@example.com",
            "username": "duplicateuser",
            "password": "password123"
        }
        
        # Primer registro
        response1 = client.post("/api/auth/register", json=user_data1)
        assert response1.status_code == 200
        
        # Segundo registro con mismo username
        response2 = client.post("/api/auth/register", json=user_data2)
        assert response2.status_code == 400
        assert "Username already taken" in response2.json()["detail"]
    
    def test_login_success(self):
        """Test login exitoso"""
        # Registrar usuario primero
        register_data = {
            "email": "logintest@example.com",
            "username": "loginuser",
            "password": "loginpass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        # Hacer login
        login_data = {
            "email": "logintest@example.com",
            "password": "loginpass123"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
    
    def test_login_wrong_password(self):
        """Test login con contraseña incorrecta"""
        # Registrar usuario primero
        register_data = {
            "email": "wrongpass@example.com",
            "username": "wrongpassuser",
            "password": "correctpass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        # Intentar login con contraseña incorrecta
        login_data = {
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_user_not_found(self):
        """Test login con usuario inexistente"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_get_current_user_profile(self):
        """Test obtener perfil del usuario actual"""
        # Registrar y hacer login
        register_data = {
            "email": "profile@example.com",
            "username": "profileuser",
            "password": "profilepass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": "profile@example.com",
            "password": "profilepass123"
        })
        token = login_response.json()["access_token"]
        
        # Obtener perfil
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "profile@example.com"
        assert data["username"] == "profileuser"
        assert data["is_active"] == True
    
    def test_get_current_user_profile_without_token(self):
        """Test obtener perfil sin token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 403  # No Authorization header
    
    def test_get_current_user_profile_invalid_token(self):
        """Test obtener perfil con token inválido"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_update_user_profile(self):
        """Test actualizar perfil de usuario"""
        # Registrar y hacer login
        register_data = {
            "email": "update@example.com",
            "username": "updateuser",
            "password": "updatepass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": "update@example.com",
            "password": "updatepass123"
        })
        token = login_response.json()["access_token"]
        
        # Actualizar username
        response = client.put(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            params={"username": "newusername"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "update@example.com"
    
    def test_change_password(self):
        """Test cambio de contraseña"""
        # Registrar y hacer login
        register_data = {
            "email": "changepass@example.com",
            "username": "changepassuser",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=register_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": "changepass@example.com",
            "password": "oldpassword123"
        })
        token = login_response.json()["access_token"]
        
        # Cambiar contraseña
        response = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "current_password": "oldpassword123",
                "new_password": "newpassword123"
            }
        )
        
        assert response.status_code == 200
        assert "Password updated successfully" in response.json()["message"]
        
        # Verificar que la nueva contraseña funciona
        new_login_response = client.post("/api/auth/login", json={
            "email": "changepass@example.com",
            "password": "newpassword123"
        })
        assert new_login_response.status_code == 200
    
    def test_change_password_wrong_current(self):
        """Test cambio de contraseña con contraseña actual incorrecta"""
        # Registrar y hacer login
        register_data = {
            "email": "wrongcurrent@example.com",
            "username": "wrongcurrentuser",
            "password": "correctpass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": "wrongcurrent@example.com",
            "password": "correctpass123"
        })
        token = login_response.json()["access_token"]
        
        # Intentar cambiar con contraseña actual incorrecta
        response = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "current_password": "wrongpassword",
                "new_password": "newpassword123"
            }
        )
        
        assert response.status_code == 400
        assert "Incorrect current password" in response.json()["detail"]
    
    def test_refresh_token(self):
        """Test renovación de token"""
        # Registrar y hacer login
        register_data = {
            "email": "refresh@example.com",
            "username": "refreshuser",
            "password": "refreshpass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": "refresh@example.com",
            "password": "refreshpass123"
        })
        token = login_response.json()["access_token"]
        
        # Renovar token
        response = client.post(
            "/api/auth/refresh-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
        
        # El nuevo token debería ser diferente al anterior
        new_token = data["access_token"]
        assert new_token != token


class TestProtectedEndpoints:
    """Tests para endpoints protegidos"""
    
    def setup_method(self):
        """Setup para cada test"""
        # Limpiar base de datos
        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()
        
        # Registrar usuario de prueba
        register_data = {
            "email": "protected@example.com",
            "username": "protecteduser",
            "password": "protectedpass123"
        }
        client.post("/api/auth/register", json=register_data)
        
        # Obtener token
        login_response = client.post("/api/auth/login", json={
            "email": "protected@example.com",
            "password": "protectedpass123"
        })
        self.token = login_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_create_page_with_auth(self):
        """Test crear página con autenticación"""
        page_data = {
            "title": "Página Autenticada",
            "slug": "pagina-autenticada",
            "subdomain": "test",
            "description": "Una página creada con autenticación",
            "config": {"theme": "modern"},
            "is_published": True
        }
        
        response = client.post(
            "/api/pages/",
            json=page_data,
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Página Autenticada"
        assert data["owner_id"] == 1  # ID del usuario creado
    
    def test_create_page_without_auth(self):
        """Test crear página sin autenticación"""
        page_data = {
            "title": "Página Sin Auth",
            "slug": "pagina-sin-auth",
            "description": "Esta debería fallar",
            "config": {"theme": "default"},
            "is_published": True
        }
        
        response = client.post("/api/pages/", json=page_data)
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]
    
    def test_update_own_page(self):
        """Test actualizar página propia"""
        # Crear página primero
        page_data = {
            "title": "Página Original",
            "slug": "pagina-original",
            "subdomain": "test",
            "description": "Descripción original",
            "config": {"theme": "default"},
            "is_published": False
        }
        
        create_response = client.post(
            "/api/pages/",
            json=page_data,
            headers=self.headers
        )
        page_id = create_response.json()["id"]
        
        # Actualizar página
        update_data = {
            "title": "Página Actualizada",
            "is_published": True
        }
        
        response = client.put(
            f"/api/pages/{page_id}",
            json=update_data,
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Página Actualizada"
        assert data["is_published"] == True
    
    def test_update_other_user_page(self):
        """Test intentar actualizar página de otro usuario"""
        # Simular página de otro usuario modificando directamente la BD
        db = TestingSessionLocal()
        from models import Page
        
        other_page = Page(
            title="Página de Otro",
            slug="pagina-de-otro",
            description="No deberías poder editar esto",
            config={"theme": "default"},
            is_published=True,
            owner_id=999  # ID de otro usuario
        )
        db.add(other_page)
        db.commit()
        page_id = other_page.id
        db.close()
        
        # Intentar actualizar
        update_data = {"title": "Página Hackeada"}
        
        response = client.put(
            f"/api/pages/{page_id}",
            json=update_data,
            headers=self.headers
        )
        
        assert response.status_code == 403
        assert "Not authorized to edit this page" in response.json()["detail"]
    
    def test_delete_own_page(self):
        """Test eliminar página propia"""
        # Crear página primero
        page_data = {
            "title": "Página a Eliminar",
            "slug": "pagina-a-eliminar",
            "subdomain": "test",
            "description": "Esta será eliminada",
            "config": {"theme": "default"},
            "is_published": False
        }
        
        create_response = client.post(
            "/api/pages/",
            json=page_data,
            headers=self.headers
        )
        page_id = create_response.json()["id"]
        
        # Eliminar página
        response = client.delete(
            f"/api/pages/{page_id}",
            headers=self.headers
        )
        
        assert response.status_code == 200
        assert "Page deleted successfully" in response.json()["message"]