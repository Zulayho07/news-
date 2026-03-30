from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

import crud
from schemas import CreateCategory, CategoryResponse, CreateNews, NewsResponse
from database import get_db, engine, Base, MEDIA_DIR


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(ap: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount(f'/{MEDIA_DIR}', StaticFiles(directory='media'), name='media')


@app.post('/category/', response_model=CategoryResponse)
async def create_category_endpoint(category: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(category, db)


@app.get('/category/', response_model=list[CategoryResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_categories(db)


@app.get('/category/{category_id}/', response_model=CategoryResponse)
async def read_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_category(category_id, db)


@app.put('/category/{category_id}/', response_model=CategoryResponse)
async def update_category_endpoint(category_id: int, category: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await crud.update_category(category_id, category, db)


@app.delete('/category/{category_id}/', response_model=dict)
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_category(category_id, db)


# --------------------------------------------------------------

@app.post('/news/', response_model=NewsResponse)
async def create_news_endpoint(theme: str, category_id: int,
                               image: UploadFile=None,
                               video: UploadFile=None,
                               file: UploadFile=None,
                               db: AsyncSession = Depends(get_db)):
    news=CreateNews(theme=theme, category_id=category_id)
    return await crud.create_news(news, db, image, video, file)


@app.get('/news/', response_model=list[NewsResponse])
async def read_news_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_news(db)


@app.get('/news/{news_id}/', response_model=NewsResponse)
async def read_new_endpoint(news_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_new(news_id, db)


@app.put('/news/{news_id}/', response_model=NewsResponse)
async def update_news_endpoint(news_id: int, news: CreateNews, db: AsyncSession = Depends(get_db)):
    return await crud.update_news(news_id, news, db)


@app.delete('/news/{news_id}/', response_model=dict)
async def delete_news_endpoint(news_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_news(news_id, db)


if __name__ == '__main__':
    uvicorn.run(app)
