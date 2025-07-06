import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base, User, Page, Component
from auth import auth_manager

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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

def setup_test_db():
    """Clean up test database"""
    db = TestingSessionLocal()
    db.query(Component).delete()
    db.query(Page).delete()
    db.query(User).delete()
    db.commit()
    db.close()

def get_auth_headers():
    """Helper function to get authentication headers"""
    # Create a test user
    db = TestingSessionLocal()
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if not existing_user:
        hashed_password = auth_manager.get_password_hash("testpassword")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(user)
        db.commit()
    db.close()
    
    # Login and get token
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Landing Builder API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_page():
    setup_test_db()
    headers = get_auth_headers()
    page_data = {
        "title": "Test Page",
        "slug": "test-page",
        "subdomain": "test",
        "description": "A test page",
        "config": {"theme": "default"},
        "is_published": False
    }
    response = client.post("/api/pages/", json=page_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Page"
    assert data["slug"] == "test-page"
    assert data["is_published"] == False
    return data["id"]

def test_get_pages():
    setup_test_db()
    headers = get_auth_headers()
    response = client.get("/api/pages/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_page():
    setup_test_db()
    headers = get_auth_headers()
    page_id = test_create_page()
    response = client.get(f"/api/pages/{page_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == page_id
    assert data["title"] == "Test Page"

def test_get_page_by_slug():
    setup_test_db()
    headers = get_auth_headers()
    test_create_page()
    response = client.get("/api/pages/slug/test-page", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "test-page"

def test_update_page():
    setup_test_db()
    headers = get_auth_headers()
    page_id = test_create_page()
    update_data = {
        "title": "Updated Test Page",
        "is_published": True
    }
    response = client.put(f"/api/pages/{page_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Page"
    assert data["is_published"] == True

def test_publish_page():
    setup_test_db()
    headers = get_auth_headers()
    page_id = test_create_page()
    response = client.post(f"/api/pages/{page_id}/publish", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_published"] == True

def test_delete_page():
    setup_test_db()
    headers = get_auth_headers()
    page_id = test_create_page()
    response = client.delete(f"/api/pages/{page_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Page deleted successfully"}

def test_create_component():
    setup_test_db()
    headers = get_auth_headers()
    page_id = test_create_page()
    component_data = {
        "type": "hero",
        "content": {"title": "Hero Title", "subtitle": "Hero subtitle"},
        "styles": {"background": "#ffffff"},
        "position": 1,
        "is_visible": True
    }
    response = client.post(f"/api/components/?page_id={page_id}", json=component_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "hero"
    assert data["content"]["title"] == "Hero Title"
    assert data["position"] == 1
    return data["id"], page_id

def test_get_page_components():
    setup_test_db()
    headers = get_auth_headers()
    component_id, page_id = test_create_component()
    response = client.get(f"/api/components/page/{page_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == component_id

def test_update_component():
    setup_test_db()
    headers = get_auth_headers()
    component_id, page_id = test_create_component()
    update_data = {
        "type": "hero",
        "content": {"title": "Updated Hero Title"},
        "styles": {"background": "#000000"},
        "position": 1,
        "is_visible": False
    }
    response = client.put(f"/api/components/{component_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["content"]["title"] == "Updated Hero Title"
    assert data["is_visible"] == False

def test_delete_component():
    setup_test_db()
    headers = get_auth_headers()
    component_id, page_id = test_create_component()
    response = client.delete(f"/api/components/{component_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Component deleted successfully"}

def test_page_not_found():
    setup_test_db()
    headers = get_auth_headers()
    response = client.get("/api/pages/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Page not found"}

def test_component_not_found():
    setup_test_db()
    headers = get_auth_headers()
    response = client.get("/api/components/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Component not found"}

def test_duplicate_slug():
    setup_test_db()
    headers = get_auth_headers()
    page_data = {
        "title": "Test Page",
        "slug": "duplicate-slug",
        "subdomain": "test",
        "description": "A test page",
        "config": {"theme": "default"},
        "is_published": False
    }
    # Primera página
    response1 = client.post("/api/pages/", json=page_data, headers=headers)
    assert response1.status_code == 200
    
    # Segunda página con mismo slug
    response2 = client.post("/api/pages/", json=page_data, headers=headers)
    assert response2.status_code == 400
    assert response2.json() == {"detail": "Ya existe una página con ese subdominio y slug"}