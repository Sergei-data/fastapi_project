from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *
from sqlalchemy import select, update, delete
from app.schemas import CreatePetCategory

from slugify import slugify
from app.utils.slug import generate_unique_slug
from app.routers.auth import get_current_user



router = APIRouter(prefix="/pet_categories", tags=["pet_categories"])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(select(PetCategory))
    categories = result.all()
    return categories




@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_category(
    create_category: CreatePetCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)] 
):
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can create categories"
        )

    base_slug = slugify(f"{create_category.animal_type}-{create_category.size}")
    unique_slug = await generate_unique_slug(db, base_slug)

    new_category = PetCategory(
        animal_type=create_category.animal_type,
        size=create_category.size,
        slug=unique_slug
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    




@router.put("/update/{category_id}")
async def update_category(
    category_id: int,
    category_data: CreatePetCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
):
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update categories"
        )

    result = await db.execute(select(PetCategory).where(PetCategory.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    base_slug = slugify(f"{category_data.animal_type}-{category_data.size}")
    unique_slug = await generate_unique_slug(db, base_slug)

    await db.execute(
        update(PetCategory)
        .where(PetCategory.id == category_id)
        .values(
            animal_type=category_data.animal_type,
            size=category_data.size,
            slug=unique_slug
        )
    )
    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Category updated successfully"
    }



@router.delete("/delete/{category_id}")
async def delete_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
):
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete categories"
        )

    result = await db.execute(select(PetCategory).where(PetCategory.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.execute(delete(PetCategory).where(PetCategory.id == category_id))
    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "detail": f"Category with id {category_id} deleted successfully"
    }