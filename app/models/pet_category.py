from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from app.backend.db import Base 
from app.models import *

class PetCategory(Base):
    __tablename__ = "pet_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    animal_type: Mapped[str] = mapped_column(String(50))  # Например: "Кошка", "Собака"
    size: Mapped[str] = mapped_column(String(50))         # Например: "Маленький", "Средний", "Большой"
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    pets: Mapped[list["Pet"]] = relationship(back_populates="category")


