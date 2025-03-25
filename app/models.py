from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    publication_time: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )


class Keyword(Base):
    __tablename__ = "keywords"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class ArticleKeyword(Base):
    __tablename__ = "keyword_article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey(Article.id))
    keyword_id: Mapped[int] = mapped_column(Integer, ForeignKey(Keyword.id))
    article: Mapped[set["Article"]] = relationship(
        Keyword, collection_class=set, backref="articles"
    )
    keyword: Mapped[set["Keyword"]] = relationship(
        Article, collection_class=set, backref="keywords"
    )
    __table_args__ = (
        UniqueConstraint("article_id", "keyword_id", name="_article_keyword_uc"),
    )
