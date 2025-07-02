from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from app.models import *

async def generate_unique_slug(db: AsyncSession, base_slug: str) -> str:
   
    slug = base_slug
    index = 1
    max_attempts = 100  
    
    for _ in range(max_attempts):
        
        result = await db.execute(select(Pet).where(Pet.slug == slug))
        if not result.scalar_one_or_none():
            return slug
        
        slug = f"{base_slug}-{index}"
        index += 1
    
    raise ValueError("Не удалось сгенерировать уникальный slug")