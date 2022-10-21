#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: crud_poetry.py
# 创建时间: 2022/10/17 0017 19:42
# 版   本：V 0.1
# 说   明: 
"""
from sqlalchemy.orm import Session
from sqlalchemy import func

from sql_app.models import Author, Poetry


def get_author_by_name(db: Session, name: str):
    return db.query(Author).filter(Author.name == name, Author.is_delete == 0).first()


def get_author_by_dynasty(db: Session, dynasty: str, skip: int = 0, limit: int = 10):
    return db.query(Author).filter(Author.dynasty == dynasty, Author.is_delete == 0).offset(skip).limit(limit).all()


def get_author_by_name_and_dynasty(db: Session, name: str, dynasty: str):
    return db.query(Author).filter(Author.name == name, Author.dynasty == dynasty, Author.is_delete == 0).first()


def get_poetry_by_author_id(db: Session, author_id: str, skip: int = 0, limit: int = 10):
    return db.query(Poetry).filter(Poetry.author_id == author_id, Poetry.is_delete == 0).offset(skip).limit(limit).all()


def get_poetry_by_name_and_author_id(db: Session, name: str, author_id: str):
    return db.query(Poetry).filter(Poetry.name == name, Poetry.author_id == author_id, Poetry.is_delete == 0).first()


def get_poetry_by_type_and_name_and_author_and_phrase(db: Session, poetry_type: str, name: str, author_id: str,
                                                      phrase: str):
    return db.query(Poetry).filter(Poetry.type == poetry_type, Poetry.name == name, Poetry.author_id == author_id,
                                   Poetry.phrase == phrase, Poetry.is_delete == 0).first()


def get_poetry_by_type(db: Session, poetry_type: str, skip: int = 0, limit: int = 10):
    return db.query(Poetry).filter(Poetry.type == poetry_type, Poetry.is_delete == 0).offset(skip).limit(limit).all()


def get_poetry_by_id(db: Session, poetry_id: str):
    return db.query(Poetry).filter(Poetry.id == poetry_id, Poetry.is_delete == 0).first()


def get_poetry_by_type_random(db: Session, poetry_type: str):
    return db.query(Poetry).filter(Poetry.type == poetry_type, Poetry.is_delete == 0).order_by(func.random()).first()

def get_poetry_by_author_name(db: Session, author_name: str):
    return db.query(Poetry).filter(Poetry.author.name == author_name, Poetry.is_delete == 0).first()


def get_poetry_by_author_name_all(db: Session, author_name: str, skip: int = 0, limit: int = 10):
    return db.query(Poetry).filter(Poetry.author.name == author_name, Poetry.is_delete == 0).offset(skip).limit(
        limit).all()


def get_poetry_by_name_and_phrase(db: Session, name: str, phrase: str):
    return db.query(Poetry).filter(Poetry.name == name, Poetry.phrase == phrase, Poetry.is_delete == 0).first()


def get_poetry(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Poetry).filter(Poetry.is_delete == 0).offset(skip).limit(limit).all()


def get_poetry_by_id(db: Session, poetry_id: str):
    return db.query(Poetry).filter(Poetry.id == poetry_id, Poetry.is_delete == 0).first()


def get_poetry_by_name(db: Session, name: str):
    return db.query(Poetry).filter(Poetry.name == name, Poetry.is_delete == 0).first()


def get_poetry_by_phrase(db: Session, phrase: str):
    return db.query(Poetry).filter(Poetry.phrase == phrase, Poetry.is_delete == 0).first()


def create_poetry(db: Session, poetry: dict):
    db_poetry = Poetry(
        type=poetry["type"],
        phrase=poetry["phrase"],
        explain=poetry["explain"],
        name=poetry["name"],
        appreciation=poetry["appreciation"],
        original=poetry["original"],
        translation=poetry["translation"],
        background=poetry["background"],
        url=poetry["url"],
        author_id=poetry["author_id"],
    )
    db.add(db_poetry)
    db.commit()
    db.refresh(db_poetry)
    return db_poetry


def add_all_poetry(db: Session, poetry_list: list):
    case = []
    for poetry in poetry_list:
        db_poetry = Poetry(
            type=poetry["type"],
            phrase=poetry["phrase"],
            explain=poetry["explain"],
            name=poetry["name"],
            appreciation=poetry["appreciation"],
            original=poetry["original"],
            translation=poetry["translation"],
            background=poetry["background"],
            url=poetry["url"],
            author_id=poetry["author_id"],
        )
        case.append(db_poetry)
    db.add_all(case)
    db.commit()


def create_author(db: Session, author: dict):
    db_author = Author(name=author["name"], dynasty=author["dynasty"], introduce=author["introduce"])
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
