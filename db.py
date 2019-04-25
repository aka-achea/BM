#!/usr/bin/env python
#coding:utf-8
#tested in win

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# customized module
# from mylog import get_funcname, mylogger
# from bm_pop import logfile,dbfile


Base = declarative_base()


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String(8))
    # article = relationship('Article')

    # def __repr__(self):
    #     return f'<{self.id} = {self.name}>'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(64))
    name = Column(String(15))
    article = relationship('Article',backref='user')

    # def __repr__(self):
    #     return f'<User {self.name} Email Address is {self.email}>'

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer,primary_key=True)
    timestamp = Column(String(100))
    title = Column(String(64))
    # link = Column(String(1000))
    # source = Column(String(64))

    # tag_id = Column(String(20),ForeignKey('tags.id'))
    user_email = Column(String(20),ForeignKey('users.email'))

    # def __repr__(self):
    #     return f'<Article name = {self.title}>'

if __name__ == "__main__":
    engine = create_engine(r'sqlite:///E:\test.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Tag.__tablename__
    Base.metadata.create_all(engine)
    # tag1 = Tag(id=2,name='GgG')
    u1 = User(email='u1@h.com',name='u1')
    session.add(u1)
 

    a1 = Article(timestamp=func.now(),title='a1',user_email='u1@h.com')
    session.add(a1)

    session.commit()

    u = session.query(User).first()
    print(u.article)
    a = session.query(Article).first()
    print(a.user_email)
    # print(u.article.title)