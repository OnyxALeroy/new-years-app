from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from typing import Optional

from app.core.security import verify_token, create_access_token
from app.core.config import settings
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserResponse, Token, LoginRequest, UserRole, UserUpdate

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_crud.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_user_auth(current_user: dict = Depends(get_current_user)) -> dict:
    return current_user


async def get_admin_user(current_user: dict = Depends(get_current_user_auth)) -> dict:
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await user_crud.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_email = await user_crud.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = await user_crud.create_user(user)
    return UserResponse(
        id=str(db_user["_id"]),
        email=db_user["email"],
        username=db_user["username"],
        role=db_user["role"],
        created_at=db_user["created_at"]
    )


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    user = await user_crud.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user_auth)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        username=current_user["username"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )


@router.get("/users", response_model=list[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_admin_user)):
    users = await user_crud.get_users(skip=skip, limit=limit)
    return [
        UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            username=user["username"],
            role=user["role"],
            created_at=user["created_at"]
        )
        for user in users
    ]


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: dict = Depends(get_admin_user)
):
    updated_user = await user_crud.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        role=updated_user["role"],
        created_at=updated_user["created_at"]
    )