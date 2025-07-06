from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from database import get_db
from models import User
from schemas import UserCreate, User as UserSchema
from auth import auth_manager, get_current_user, get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Schemas específicos para autenticación
from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=UserProfile)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    
    # Verificar que el email no exista
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Verificar que el username no exista
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Crear nuevo usuario
    hashed_password = auth_manager.get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserProfile(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        is_active=db_user.is_active,
        created_at=db_user.created_at.isoformat()
    )

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Iniciar sesión de usuario"""
    
    user = auth_manager.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=30)
    access_token = auth_manager.create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=1800  # 30 minutos en segundos
    )

@router.get("/me", response_model=UserProfile)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Obtener perfil del usuario actual"""
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )

@router.put("/me", response_model=UserProfile)
def update_user_profile(
    username: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar perfil del usuario actual"""
    
    if username:
        # Verificar que el username no esté tomado por otro usuario
        existing_user = db.query(User).filter(
            User.username == username,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        current_user.username = username
    
    db.commit()
    db.refresh(current_user)
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )

@router.post("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario"""
    
    # Verificar contraseña actual
    if not auth_manager.verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Actualizar contraseña
    current_user.hashed_password = auth_manager.get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.post("/refresh-token", response_model=Token)
def refresh_access_token(current_user: User = Depends(get_current_user)):
    """Renovar token de acceso"""
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Crear nuevo token
    access_token_expires = timedelta(minutes=30)
    access_token = auth_manager.create_access_token(
        data={"sub": current_user.email}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=1800
    )

@router.delete("/me")
def delete_user_account(
    password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar cuenta del usuario (requiere confirmación de contraseña)"""
    
    # Verificar contraseña
    if not auth_manager.verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    # Marcar como inactivo en lugar de eliminar (soft delete)
    current_user.is_active = False
    db.commit()
    
    return {"message": "Account deactivated successfully"}