"""Resource queries and response shaping."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Resource
from app.schemas.schemas import ResourceDetail, ResourceListItem, ResourceSection


def to_resource_detail(resource: Resource) -> ResourceDetail:
    sections = [ResourceSection.model_validate(s) for s in (resource.sections or [])]
    return ResourceDetail(
        id=resource.id,
        title=resource.title,
        slug=resource.slug,
        topic_area=resource.topic_area,
        difficulty_level=resource.difficulty_level,
        summary=resource.summary,
        sections=sections,
        order=resource.order,
    )


async def list_resources(db: AsyncSession) -> list[Resource]:
    result = await db.execute(select(Resource).order_by(Resource.order))
    return list(result.scalars().all())


async def get_resource_by_slug(db: AsyncSession, slug: str) -> Resource | None:
    result = await db.execute(select(Resource).where(Resource.slug == slug))
    return result.scalar_one_or_none()
