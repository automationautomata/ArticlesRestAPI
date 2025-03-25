import uvicorn
from fastapi import FastAPI

from app import constants
from app.routers.article_keywords import router as article_keywords_router
from app.routers.articles import router as articles_router
from app.routers.keywords import router as keywords_router

if __name__ == "__main__":
    app = FastAPI()

    app.include_router(articles_router)
    app.include_router(keywords_router)
    app.include_router(article_keywords_router)

    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
