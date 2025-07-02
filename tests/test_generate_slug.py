import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.slug import generate_unique_slug

class FakeResult:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value

@pytest.mark.asyncio
async def test_generate_unique_slug():
    
    db = AsyncMock(spec=AsyncSession)

    
    db.execute.side_effect = [
        FakeResult("exists"),  
        FakeResult(None)       
    ]

    slug = await generate_unique_slug(db, "cat-small")
    assert slug == "cat-small-1"
