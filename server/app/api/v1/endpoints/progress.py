from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import ProgressResponse
from app.services.progress import get_user_progress

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/", response_model=ProgressResponse)
async def get_progress(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProgressResponse:
    return await get_user_progress(db, current_user)
