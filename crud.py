from pathlib import Path
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile


from schemas import (CreateCategory, CategoryResponse,
                     CreateNews, NewsResponse)
from models import News, Category
from database import MEDIA_DIR

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


async def create_news(news: CreateNews, db: AsyncSession,
image: UploadFile=None, video: UploadFile=None, file: UploadFile=None) -> NewsResponse:
    if image:
        if image.filename.lower().split('.')[-1] not in ['jpeg', 'jpg', 'png', 'img', 'bmp']:
            raise HTTPException(status_code=404, detail='Only jpg, png, bmp, jpeg images are allowed.')

    if video:
        if video.filename.lower().split('.')[-1] not in ['mp4', 'avi', 'mov']:
            raise HTTPException(status_code=404, detail='Only mp4, avi, mov videos are allowed.')

    db_news = News(**news.model_dump())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)

    if image:
        image_path=Path(MEDIA_DIR) / f'news_{db_news.id}_image.{image.filename.split('.')[-1]}'
        with image_path.open(mode='wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

            db_news.image=str(image_path)


        if video:
            video_path = Path(MEDIA_DIR) / f'news_{db_news.id}_video.{video.filename.split('.')[-1]}'
            with video_path.open(mode='wb') as buffer:
                shutil.copyfileobj(video.file, buffer)

            db_news.video=str(video_path)

        if file:
            file_path = Path(MEDIA_DIR) / f'news_{db_news.id}_file.{file.filename.split('.')[-1]}'
            with file_path.open(mode='wb') as buffer:
                shutil.copyfileobj(file.file, buffer)

            db_news.file=str(file_path)


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
