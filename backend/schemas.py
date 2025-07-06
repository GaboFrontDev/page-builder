from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ComponentBase(BaseModel):
    type: str
    content: Dict[str, Any]
    styles: Optional[Dict[str, Any]] = {}
    position: int
    is_visible: bool = True

class ComponentCreate(ComponentBase):
    pass

class ComponentUpdate(BaseModel):
    type: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    styles: Optional[Dict[str, Any]] = None
    position: Optional[int] = None
    is_visible: Optional[bool] = None

class Component(ComponentBase):
    id: int
    page_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PageBase(BaseModel):
    title: str
    slug: str
    subdomain: str
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = {}
    is_published: bool = False

class PageCreate(PageBase):
    pass

class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    subdomain: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None

class Page(PageBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    components: List[Component] = []
    
    class Config:
        from_attributes = True

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    config: Dict[str, Any]
    is_premium: bool = False

class Template(TemplateBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    filename: str
    original_name: str
    file_type: str
    file_size: int
    url: str

class Asset(AssetBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True