from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ArticleKeyword
from app.schemas import ArticleKeywordsSchema

router = APIRouter(prefix="/article_keywords")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_keywords_to_article(
    article_keywords: ArticleKeywordsSchema, db: Session = Depends(get_db)
):
    data = article_keywords.model_dump()
    article_id = data["article_id"]

    new_records = []
    for id in data["keywords"]:
        new_records.append(ArticleKeyword(article_id=article_id, keyword_id=id))
        db.add(new_records[-1])

    db.commit()
    for record in new_records:
        db.refresh(record)
        
    return new_records
