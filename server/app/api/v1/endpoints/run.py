from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.rate_limit import get_user_or_remote_address, limiter
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import RunRequest, RunResponse
from app.services.run import run_exercise_code

router = APIRouter(prefix="/run", tags=["run"])


@router.post("/", response_model=RunResponse)
@limiter.limit("30/minute", key_func=get_user_or_remote_address)
async def run_code(
    request: Request,
    payload: RunRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RunResponse:
    """Run code in the exercise's language and return its output (not graded or saved)."""
    try:
        return await run_exercise_code(db, payload.exercise_id, payload.code, payload.input_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
