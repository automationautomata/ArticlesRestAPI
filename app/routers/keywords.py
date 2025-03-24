from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from database import get_db
from models import Article, ArticleKeyword, Keyword
from schemas import KeywordSchema, ListArticlesResponse, ListKeywordsResponse

router = APIRouter(prefix="/keywords")


@router.get("/", response_model=ListKeywordsResponse)
async def get_keywords(
    db: Session = Depends(get_db),
    limit: int = Query(default=1),
    offset: int = Query(default=0),
    sort_order: bool = Query(default=True),
    sort_by_id: bool = Query(default=False),
):
    sort_field = Keyword.word if not sort_by_id else Keyword.id
    if not sort_order:
        sort_field = sort_field.desc()
    keywords = db.query(Keyword).order_by(sort_field).offset(offset).limit(limit).all()
    return keywords


@router.get("/existing", response_model=ListKeywordsResponse)
async def check_keywords_existence(
    keywords: list[str] = Query(),
    db: Session = Depends(get_db),
):
    existing_keywords = db.query(Keyword).filter(Keyword.word.in_(keywords)).all()
    return existing_keywords


@router.get("/simular", response_model=ListKeywordsResponse)
async def get_simular_keywords(
    keyword: list[str] = Query(),
    db: Session = Depends(get_db),
):
    simular_keywords = db.query(Keyword).filter(Keyword.word.like(keyword)).all()
    return simular_keywords


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=KeywordSchema
)
async def create_article(keyword: KeywordSchema, db: Session = Depends(get_db)):
    new_keyword = Keyword(**keyword.model_dump())
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)
    return new_keyword


@router.get("/{id}/articles", response_model=ListArticlesResponse)
async def get_articles_by_keyword(
    id: int,
    db: Session = Depends(get_db),
    limit: int = Query(default=1),
    offset: int = Query(default=0),
):
    articles = (
        db.query(Article)
        .join(ArticleKeyword, ArticleKeyword.article == Article.id)
        .filter(ArticleKeyword.keyword == id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return articles
