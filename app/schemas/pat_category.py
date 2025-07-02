from pydantic import BaseModel


class CreatePetCategory(BaseModel):
    animal_type: str           
    size: str                