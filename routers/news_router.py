from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, Depends, APIRouter
from schemas import NewsResponse, CreateNews, NewsPartialUpdate, NewsDeleteResponse
from database import get_db
import crud

router = APIRouter()


@router.post('/', response_model=NewsResponse)
async def create_news_endpoint(theme: str, category_id: int,
                               image: UploadFile = None,
                               video: UploadFile = None,
                               file: UploadFile = None,
                               db: AsyncSession = Depends(get_db)):
    news = CreateNews(theme=theme, category_id=category_id)
    return await crud.create_news(news, db, image, video, file)


@router.get('/', response_model=list[NewsResponse])
async def read_news_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_news(db)


@router.get('/{news_id}/', response_model=NewsResponse)
async def read_new_endpoint(news_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_new(news_id, db)


@router.put('/{news_id}/', response_model=NewsResponse)
async def update_news_endpoint(news_id: int, news: CreateNews, db: AsyncSession = Depends(get_db)):
    return await crud.update_news(news_id, news, db)


@router.patch('/{news_id}/', response_model=NewsResponse)
async def update_news_endpoint(news_id: int, news: NewsPartialUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.partial_update_news(news_id, news, db)


@router.delete('/{news_id}/', response_model=NewsDeleteResponse)
async def delete_news_endpoint(news_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_news(news_id, db)
