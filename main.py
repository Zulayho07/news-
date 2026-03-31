from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from database import engine, Base, MEDIA_DIR
from routers.category_router import router as category_router
from routers.news_router import router as news_router


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(ap: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.mount(f'/{MEDIA_DIR}', StaticFiles(directory='media'), name='media')

app.include_router(category_router, tags=['Category'], prefix='/category')
app.include_router(news_router, tags=['News'], prefix='/news')

if __name__ == '__main__':
    uvicorn.run(app)
