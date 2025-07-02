
from pydantic import BaseModel


class CreatePet(BaseModel):
    name: str
    description: str
    age: int
    breed: str
    color: str
    image_url: str         
    category_id: int           
