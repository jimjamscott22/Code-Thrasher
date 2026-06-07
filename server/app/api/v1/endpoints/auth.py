from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def build_token_response(user: User) -> Token:
    return Token(
        access_token=create_access_token(str(user.id)),
        token_type="bearer",
        user=UserOut.model_validate(user),
    )


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    username_result = await db.execute(
        select(User).where(User.username == payload.username)
    )
    if username_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already registered",
        )

    email_result = await db.execute(
        select(User).where(func.lower(User.email) == str(payload.email).lower())
    )
    if email_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    user = User(
        username=payload.username,
        email=str(payload.email),
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return build_token_response(user)


@router.post("/login", response_model=Token)
async def login(
    payload: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    identifier = payload.username_or_email
    result = await db.execute(
        select(User).where(
            or_(
                User.username == identifier,
                func.lower(User.email) == identifier.lower(),
            )
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return build_token_response(user)


@router.get("/me", response_model=UserOut)
async def read_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
