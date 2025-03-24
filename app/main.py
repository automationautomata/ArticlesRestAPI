from fastapi import FastAPI
import uvicorn

import constants
from routers.articles import router as articles_router
from routers.keywords import router as keywords_router
from routers.article_keywords import router as article_keywords_router

if __name__ == "__main__":
    app = FastAPI()

    app.include_router(articles_router)
    app.include_router(keywords_router)
    app.include_router(article_keywords_router)

    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
