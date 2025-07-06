import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base

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

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Landing Builder API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_page():
    page_data = {
        "title": "Test Page",
        "slug": "test-page",
        "description": "A test page",
        "config": {"theme": "default"},
        "is_published": False
    }
    response = client.post("/api/pages/", json=page_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Page"
    assert data["slug"] == "test-page"
    assert data["is_published"] == False
    return data["id"]

def test_get_pages():
    response = client.get("/api/pages/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_page():
    page_id = test_create_page()
    response = client.get(f"/api/pages/{page_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == page_id
    assert data["title"] == "Test Page"

def test_get_page_by_slug():
    test_create_page()
    response = client.get("/api/pages/slug/test-page")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "test-page"

def test_update_page():
    page_id = test_create_page()
    update_data = {
        "title": "Updated Test Page",
        "is_published": True
    }
    response = client.put(f"/api/pages/{page_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Page"
    assert data["is_published"] == True

def test_publish_page():
    page_id = test_create_page()
    response = client.post(f"/api/pages/{page_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Page published successfully"
    assert data["page"]["is_published"] == True

def test_delete_page():
    page_id = test_create_page()
    response = client.delete(f"/api/pages/{page_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Page deleted successfully"}

def test_create_component():
    page_id = test_create_page()
    component_data = {
        "type": "hero",
        "content": {"title": "Hero Title", "subtitle": "Hero subtitle"},
        "styles": {"background": "#ffffff"},
        "position": 1,
        "is_visible": True
    }
    response = client.post(f"/api/components/?page_id={page_id}", json=component_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "hero"
    assert data["content"]["title"] == "Hero Title"
    assert data["position"] == 1
    return data["id"], page_id

def test_get_page_components():
    component_id, page_id = test_create_component()
    response = client.get(f"/api/components/page/{page_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == component_id

def test_update_component():
    component_id, page_id = test_create_component()
    update_data = {
        "type": "hero",
        "content": {"title": "Updated Hero Title"},
        "styles": {"background": "#000000"},
        "position": 1,
        "is_visible": False
    }
    response = client.put(f"/api/components/{component_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"]["title"] == "Updated Hero Title"
    assert data["is_visible"] == False

def test_delete_component():
    component_id, page_id = test_create_component()
    response = client.delete(f"/api/components/{component_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Component deleted successfully"}

def test_page_not_found():
    response = client.get("/api/pages/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Page not found"}

def test_component_not_found():
    response = client.get("/api/components/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Component not found"}

def test_duplicate_slug():
    page_data = {
        "title": "Test Page",
        "slug": "duplicate-slug",
        "description": "A test page",
        "config": {"theme": "default"},
        "is_published": False
    }
    # Primera página
    response1 = client.post("/api/pages/", json=page_data)
    assert response1.status_code == 200
    
    # Segunda página con mismo slug
    response2 = client.post("/api/pages/", json=page_data)
    assert response2.status_code == 400
    assert response2.json() == {"detail": "Slug already exists"}