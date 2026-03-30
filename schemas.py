from pydantic import BaseModel
from typing import Optional


class CreateCategory(BaseModel):
    name: str


class CategoryResponse(CreateCategory):
    id: int

    class Config:
        from_attributes = True


class CreateNews(BaseModel):
    theme: str
    image: Optional[str] = None
    video: Optional[str] = None
    file:Optional[str]=None
    category_id: int


class NewsResponse(CreateNews):
    id: int


    class Config:
        from_attributes = True
