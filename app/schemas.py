from datetime import datetime
from pydantic import BaseModel

from typing import List, Optional


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    text: str
    publication_time: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class KeywordSchema(BaseModel):
    id: Optional[int] = None
    word: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# class KeywordSchema(NewKeywordSchema):
#     id: int


class ArticleKeywordsSchema(BaseModel):
    article_id: int
    keyword_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListArticlesResponse(BaseModel):
    articles: List[ArticleSchema]


class ListKeywordsResponse(BaseModel):
    keywords: List[KeywordSchema]
