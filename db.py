#!/usr/bin/env python
#coding:utf-8
#tested in win

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# customized module
# from mylog import get_funcname, mylogger
# from bm_pop import logfile,dbfile




Base = declarative_base()


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String(20))
    article = relationship('Article')

    def __repr__(self):
        return f'<{self.id} = {self.name}>'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(80))
    name = Column(String(15))
    article = relationship('Article')

    def __repr__(self):
        return f'<User {self.name} Email Address is {self.email}>'

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer,primary_key=True)
    title = Column(String(20))
    time = Column(String(100))
    link = Column(String(1000))
    tagid = Column(String(20),ForeignKey('tags.id'))
    email = Column(String(80),ForeignKey('users.id'))

    def __repr__(self):
        return f'<Tag name = {self.name}>'

if __name__ == "__main__":
    engine = create_engine(r'sqlite:///E:\test.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    Tag.__tablename__
    Base.metadata.create_all(engine)
    # tag1 = Tag(id=2,name='GgG')
    # session.add(tag1)
    # session.commit()
    a = session.query(Tag).all()
    print(a)