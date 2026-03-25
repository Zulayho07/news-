from  pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str

class CategoryResponse(CreateCategory):
    id: int

    class Config:
        from_attributes=True


class CreateNews(BaseModel):
    name: str


class NewsResponse(CreateNews):
    id: int
    theme: str
    category_id:int

    class Config:
        from_attributes = True
