#!/usr/bin/env python
#coding:utf-8
#tested in win

__version__ = 20200804

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, func
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


Base = declarative_base()


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String(4),unique=True,nullable=False)
    fullname = Column(String(8),unique=True,nullable=True)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer,primary_key=True)
    name = Column(String(16),unique=True,nullable=False)
    fullname = Column(String(16),unique=True,nullable=True)

    def __repr__(self):
        return f'<{self.id} : {self.fullname}>'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(64),unique=True,nullable=False)
    name = Column(String(15),unique=True,nullable=False)
    password_hash = Column(String(128),nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def show_hash(self):
        return print(self.password_hash)

    def __repr__(self):
        return f'<{self.name} : {self.email}>'


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer,primary_key=True)
    timestamp = Column(String(100))
    title = Column(String(64),nullable=False,index=True)
    link = Column(String(1000),nullable=False,index=True)
    author = Column(String(20),nullable=True,index=True)
    tag_id = Column(String(20),ForeignKey('tags.id'),nullable=False)
    tag = relationship('Tag',backref='articles')
    src_id = Column(String(20),ForeignKey('sources.id'),nullable=False)
    src = relationship('Source',backref='articles')
    user_id = Column(String(20),ForeignKey('users.id'),nullable=False) 
    user = relationship('User',backref='articles')

    def __repr__(self):
        return f'<{self.title} : {self.tag.fullname}>'


