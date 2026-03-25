from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from schemas import (CreateCategory, CategoryResponse,
                     CreateNews, NewsResponse)
from models import News, Category


async def create_category(category: CreateCategory, db: AsyncSession) -> CategoryResponse:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def read_categories(db: AsyncSession) -> list[CategoryResponse]:
    result = await db.execute(select(Category))
    return [CategoryResponse.model_validate(category) for category in result.scalars().all()]


async def read_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    return CategoryResponse.model_validate(category)


async def update_category(category_id: int, category: CreateCategory, db: AsyncSession) -> CategoryResponse:
    db_category = await db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    for attr, value in category.__dict__.items():
        setattr(db_category, attr, value)

    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def delete_category(category_id: int, db: AsyncSession) -> dict:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    await db.delete(category)
    await db.commit()

    return {'message': 'Category Deleted Successfully'}




# ------------------------NEWS-------------------------


async def create_news(news: CreateNews, db: AsyncSession) -> NewsResponse:
    db_news = News(**news.model_dump())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return NewsResponse.model_validate(db_news)


async def read_news(db: AsyncSession) -> list[NewsResponse]:
    result = await db.execute(select(News))
    return [NewsResponse.model_validate(news) for news in result.scalars().all()]


async def read_new(news_id: int, db: AsyncSession) -> NewsResponse:
    news = await db.get(News, news_id)
    if not news:
        raise HTTPException(status_code=404, detail='News not found')

    return NewsResponse.model_validate(news)


async def update_news(news_id: int, news: CreateNews, db: AsyncSession) -> NewsResponse:
    db_news = await db.get(News, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail='News not found')

    for attr, value in news.__dict__.items():
        setattr(db_news, attr, value)

    await db.commit()
    await db.refresh(db_news)
    return NewsResponse.model_validate(db_news)


async def delete_news(news_id: int, db: AsyncSession) -> dict:
    news = await db.get(News, news_id)
    if not news:
        raise HTTPException(status_code=404, detail='News not found')

    await db.delete(news)
    await db.commit()

    return {'message': 'News Deleted Successfully'}
