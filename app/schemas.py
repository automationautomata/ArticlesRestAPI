from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    text: str
    publication_time: Optional[datetime] = None

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
        

class ArticleKeywordsSchema(BaseModel):
    article_id: int
    keywords: List[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListArticlesResponse(BaseModel):
    articles: List[ArticleSchema]


class ListKeywordsResponse(BaseModel):
    keywords: List[KeywordSchema]
