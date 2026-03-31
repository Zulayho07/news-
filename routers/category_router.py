from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter

import crud
from schemas import CreateCategory, CategoryResponse, CategoryPartialUpdate, CategoryDeleteResponse
from database import get_db

router = APIRouter()


@router.post('/', response_model=CategoryResponse)
async def create_category_endpoint(category: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(category, db)


@router.get('/', response_model=list[CategoryResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_categories(db)


@router.get('/{category_id}/', response_model=CategoryResponse)
async def read_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_category(category_id, db)


@router.put('/{category_id}/', response_model=CategoryResponse)
async def update_category_endpoint(category_id: int, category: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await crud.update_category(category_id, category, db)


@router.patch('/{category_id}/', response_model=CategoryPartialUpdate)
async def update_category_endpoint(category_id: int, category: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await crud.partial_update_category(category_id, category, db)


@router.delete('/{category_id}/', response_model=CategoryDeleteResponse)
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_category(category_id, db)
