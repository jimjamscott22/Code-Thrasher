from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.models import Resource
from app.schemas.schemas import ResourceDetail, ResourceListItem
from app.services import resources as resource_service

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=list[ResourceListItem])
async def list_resources(db: AsyncSession = Depends(get_db)) -> list[Resource]:
    return await resource_service.list_resources(db)


@router.get("/{slug}", response_model=ResourceDetail)
async def get_resource(slug: str, db: AsyncSession = Depends(get_db)) -> ResourceDetail:
    resource = await resource_service.get_resource_by_slug(db, slug)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource_service.to_resource_detail(resource)
