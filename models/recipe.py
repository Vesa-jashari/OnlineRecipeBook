from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    name: str
    description: Optional[str]
    ingredients: str
    instructions: str
    cusine: str
    difficulty: str
    category_id: Optional[str]

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
