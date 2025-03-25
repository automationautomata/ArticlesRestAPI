from datetime import datetime

from database import get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from app.models import Article, ArticleKeyword, Keyword
from app.schemas import ArticleSchema, ListKeywordsResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/articles")


@router.get("/")
async def get_articles(
    limit: int = Query(default=1),
    offset: int = Query(default=0),
    sort_order: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    sort_field = Article.publication_time
    if not sort_order:
        sort_field = sort_field.desc()
    query = db.query(Article).order_by(sort_field).limit(limit).offset(offset)
    return query.all()


@router.get("/{id}")
async def get_article(id: int, db: Session = Depends(get_db)):
    article: Article = db.query(Article).get(id)
    return article


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleSchema, db: Session = Depends(get_db)):
    new_article = Article(**article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.patch("/{id}")
async def update_article(
    id: int, article: ArticleSchema, db: Session = Depends(get_db)
):
    query = db.query(Article).filter(Article.id == id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No article with this id: {id} is not found",
        )
    update_article = article.model_dump(exclude_unset=True)

    query.filter(Article.id == id).update(update_article, synchronize_session=False)

    db.commit()
    db.refresh(update_article)
    return article


@router.delete("/{id}")
def delete_post(id: str, db: Session = Depends(get_db)):
    query = db.query(Article).filter(Article.id == id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with this id: {id} found",
        )

    query.filter(Article.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}/keywords")#, response_model=ListKeywordsResponse)
async def get_article_keywords(
    id: int,
    db: Session = Depends(get_db),
    limit: int = Query(default=1),
    offset: int = Query(default=0),
):
    article = db.query(Article).get(id)
    keywords = list(article.keywords)

    if offset >= len(keywords):
        return []
    real_limit = max(limit+offset, len(keywords)-1)

    return keywords[offset:real_limit]


@router.get("/publications")
async def get_articles_publications(
    start_time: datetime = Query(default=datetime.now()),
    end_time: datetime = Query(default=datetime.now()),
    limit: int = Query(default=1),
    offset: int = Query(default=0),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Article)
        .filter(
            Article.publication_time > start_time,
            Article.publication_time < end_time,
        )
        .limit(limit)
        .offset(offset)
    )
    return query.all()
