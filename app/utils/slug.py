from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from app.models import *





async def generate_unique_slug(db: AsyncSession, base_slug: str) -> str:
    slug = base_slug
    index = 1
    while True:
        result = await db.execute(select(PetCategory).where(PetCategory.slug == slug))
        existing = result.scalar_one_or_none()
        if not existing:
            return slug
        slug = f"{base_slug}-{index}"
        index += 1




