from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import jwt

from app.models.users import User as UserModel
from app.db_depends import get_async_db
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user
)
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import UserCreate, User as UserSchema, RefreshTokenRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Регистрирует нового пользователя с ролью 'buyer' или 'seller'.
    """
    # Проверка уникальности email
    result = await db.scalars(select(UserModel).where(UserModel.email == user.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Создание объекта пользователя с хешированным паролем
    db_user = UserModel(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    await db.commit()
    return db_user


@router.post("/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Аутентифицирует пользователя и возвращает access_token и refresh_token.
    """
    result = await db.scalars(
        select(UserModel).where(
            UserModel.email == form_data.username,
            UserModel.is_active == True
        )
    )
    user = result.first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём access-токен
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )

    # Создаём refresh-токен с jti и token_version
    jti = str(uuid.uuid4())
    refresh_token = create_refresh_token(
        data={
            "sub": user.email,
            "role": user.role,
            "id": user.id,
            "jti": jti,
            "token_version": user.token_version,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh-token")
async def refresh_token(
        body: RefreshTokenRequest,
        db: AsyncSession = Depends(get_async_db),
):
    """
    Обновляет пару токенов (access + refresh) по старому refresh-токену.
    Старый refresh-токен инвалидируется.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    old_refresh_token = body.refresh_token

    # 1. Декодируем и проверяем старый refresh-токен
    try:
        payload = jwt.decode(old_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        token_version: int | None = payload.get("token_version")

        # Проверяем, что токен действительно refresh
        if email is None or token_type != "refresh" or token_version is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    # 2. Проверяем пользователя
    result = await db.scalars(
        select(UserModel).where(
            UserModel.email == email,
            UserModel.is_active == True
        )
    )
    user = result.first()
    if user is None:
        raise credentials_exception

    # 3. Проверяем token_version (инвалидация всех токенов пользователя)
    if token_version != user.token_version:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Инвалидируем ВСЕ старые refresh-токены пользователя
    # (увеличиваем token_version)
    user.token_version += 1
    await db.commit()

    # 5. Создаём НОВЫЙ access-токен
    new_access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )

    # 6. Создаём НОВЫЙ refresh-токен с новой версией
    new_jti = str(uuid.uuid4())
    new_refresh_token = create_refresh_token(
        data={
            "sub": user.email,
            "role": user.role,
            "id": user.id,
            "jti": new_jti,
            "token_version": user.token_version,  # новая версия
        }
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }