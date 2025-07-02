from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from app.backend.db import Base
from app.models import *

class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(100))                  # Pet's name
    description: Mapped[str] = mapped_column(String(255))           # Description of the pet
    age: Mapped[int] = mapped_column()                              # Age of the pet in years
    breed: Mapped[str] = mapped_column(String(100))                 # Breed of the pet
    color: Mapped[str] = mapped_column(String(50))                  # Color of the pet
    cuteness_rating: Mapped[float] = mapped_column(default=0.0)     # Cuteness rating from 0.0 to 10.0
    image_url: Mapped[str] = mapped_column(String(255))             # URL of the pet's image
    category_id: Mapped[int] = mapped_column(ForeignKey("pet_categories.id"))   
    slug: Mapped[str] = mapped_column(String(100), unique=True)    

    category: Mapped["PetCategory"] = relationship(back_populates="pets")