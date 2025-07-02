from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *
from sqlalchemy import insert, select, update
from app.schemas import CreatePet
from app.utils.slug_pet import generate_unique_slug
from slugify import slugify
from app.routers.auth import get_current_user


router = APIRouter(prefix="/pets", tags=["pets"])


@router.get('/{category_id}')
async def get_pets_by_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.scalars(select(Pet).where(Pet.category_id == category_id))
    pets = result.all()

    if not pets:
        raise HTTPException(status_code=404, detail="Pets not found for this category")

    return pets



@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: CreatePet,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not (current_user.get('is_admin') or current_user.get('is_supplier')):
        raise HTTPException(
            status_code=403,
            detail="Only admin or supplier users can create pets"
        )

    try:
        category = await db.get(PetCategory, pet_data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        base_slug = slugify(f"{pet_data.name}-{category.animal_type}")
        unique_slug = await generate_unique_slug(db, base_slug)

        existing = await db.execute(select(Pet).where(Pet.slug == unique_slug))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Slug already exists (race condition)")

        new_pet = Pet(
            name=pet_data.name,
            description=pet_data.description,
            age=pet_data.age,
            breed=pet_data.breed,
            color=pet_data.color,
            image_url=str(pet_data.image_url),
            category_id=pet_data.category_id,
            slug=unique_slug
        )

        db.add(new_pet)
        await db.commit()
        await db.refresh(new_pet)
        
        return new_pet

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



@router.delete('/delete/{pet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    if not (current_user.get('is_admin') or current_user.get('is_supplier')):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or supplier users can delete pets"
        )

    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with id {pet_id} not found"
        )

    try:
        await db.delete(pet)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting pet: {str(e)}"
        )

    return None