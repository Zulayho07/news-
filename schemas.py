from pydantic import BaseModel
from typing import Optional


class CreateCategory(BaseModel):
    name: str


class CategoryResponse(CreateCategory):
    id: int
    news: list['NestedNewsForCategory']

    class Config:
        from_attributes = True


class CategoryPartialUpdate(BaseModel):
    name: Optional[str]=None


class CategoryDeleteResponse(BaseModel):
    message: str


class CreateNews(BaseModel):
    theme: str
    image: Optional[str] = None
    video: Optional[str] = None
    file: Optional[str] = None
    category_id: int


class NestedCategoryForNews(BaseModel):
    id:int
    name: str


class NewsResponse(CreateNews):
    id: int
    category: NestedCategoryForNews

    class Config:
        from_attributes = True


class NestedNewsForCategory(CreateNews):
    id: int

    class Config:
        from_attributes = True


class NewsPartialUpdate(BaseModel):
    theme: Optional[str] = None
    image: Optional[str] = None
    video: Optional[str] = None
    file: Optional[str] = None
    category_id: Optional[int] = None


class NewsDeleteResponse(BaseModel):
    message: str
