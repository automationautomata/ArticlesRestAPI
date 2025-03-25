from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Article, Keyword
from app.schemas import KeywordSchema, ListArticlesResponse, ListKeywordsResponse

router = APIRouter(prefix="/keywords")


@router.get("/", response_model=ListKeywordsResponse)
async def get_keywords(
    db: Session = Depends(get_db),
    limit: int = Query(default=1, ge=1),
    offset: int = Query(default=0, ge=0),
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=KeywordSchema)
async def create_article(keyword: KeywordSchema, db: Session = Depends(get_db)):
    new_keyword = Keyword(**keyword.model_dump())
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)
    return new_keyword


@router.patch("/{id}")
async def update_article(
    id: int, article: KeywordSchema, db: Session = Depends(get_db)
):
    query = db.query(Article).filter(Article.id == id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No keyword with this id: {id} is not found",
        )
    update_article = article.model_dump(exclude_unset=True)

    query.filter(Article.id == id).update(update_article, synchronize_session=False)

    db.commit()
    db.refresh(update_article)
    
    return article


@router.get("/{id}/articles")  # , response_model=ListArticlesResponse)
async def get_articles_by_keyword(
    id: int,
    db: Session = Depends(get_db),
    limit: int = Query(default=1, ge=1),
    offset: int = Query(default=0, ge=0),
):
    record: Keyword = db.query(Keyword).get(id)
    return list(record.articles)[offset : limit + offset]
