#!/usr/bin/env python
#coding:utf-8
#tested in win


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String(8),unique=True,nullable=False)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer,primary_key=True)
    name = Column(String(16),unique=True,nullable=False)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(64),unique=True,nullable=False)
    name = Column(String(15),unique=True,nullable=False)
    password_hash = Column(String(128),nullable=False)


    def __repr__(self):
        return f'<{self.name} : {self.email}>'


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer,primary_key=True)
    timestamp = Column(String(100))
    title = Column(String(64),nullable=False,index=True)
    link = Column(String(1000),nullable=False,index=True)
    tag_id = Column(String(20),ForeignKey('tags.id'),nullable=False)
    tag = relationship('Tag',backref='articles')
    src_id = Column(String(20),ForeignKey('sources.id'),nullable=False)
    src = relationship('Source',backref='articles')
    user_id = Column(String(20),ForeignKey('users.id'),nullable=False) 
    user = relationship('User',backref='articles')

    def __repr__(self):
        return f'<{self.title} : {self.tag.name} : {self.user.name}>'


class DataBase():
    def __init__(self,dbfile):
        engine = create_engine(r'sqlite:///'+dbfile)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()        

    def reset_db(self):
        pass

    def query_tagid(self,tagname):
        return self.session.query(Tag).filter_by(name=tagname).first().id

    def query_userid(self,username):
        return self.session.query(User).filter_by(name=username).first().id

    def query_srcid(self,sourcename):
        return self.session.query(Source).filter_by(name=sourcename).first().id

    def query_userarticle_bytitle(self,user,title):
        u = self.session.query(User).filter_by(name=user).first()
        articles = []
        for f in u.articles:
            if title in f.title:
                articles.append(f)
        return articles

    def insert_src(self,sourcename):
        s = Source(name=sourcename)
        self.session.add(s)
        self.session.commit()

    def insert_tag(self,tagname):
        t = Tag(name=tagname)
        self.session.add(t)
        self.session.commit()   

    def insert_user(self,email,username):
        u = User(email=email,name=username)
        self.session.add(u)
        self.session.commit()  

    def insert_article(self,article_dict):
        timestamp = article_dict['timestamp']
        title = article_dict['title']
        tagid = self.query_tagid(article_dict['tag'])
        userid = self.query_userid(article_dict['user'])
        link = article_dict['link']
        src_id = self.query_srcid(article_dict['source'])
        article = Article(timestamp=timestamp,title=title,tag_id=tagid,user_id=userid,link=link,src_id=src_id)
        self.session.add(article)
        self.session.commit()


def test():
    # test case
    db = DataBase(dbfile)
    for x in ['t1','t2','t3']:
        db.insert_tag(x)
    for s in ['wx','mm']:
        db.insert_src(s)
    for u in [('u1@h.com','u1'),('u2@h.com','u2')]:
        db.insert_user(email=u[0],username=u[1])

    t = db.session.query(Tag).all()
    print(t)
    u = db.session.query(User).all()
    print(u)
    s = db.session.query(Source).all()
    print(s)

    a1 = {'timestamp':func.now(),'title':'testtitle','tag':'t1','user':'u2','link':'aaaaa','source':'mm'}
    db.insert_article(a1)
    a = db.query_userarticle_bytitle('u2','test')
    print(a)

    for x in a:
        print(x.link)

if __name__ == "__main__":
    import os
    dbfile = r'C:\Business\GitHub\BM\fkweb\note-dev.sqlite'
    # os.remove(dbfile)

    # engine = create_engine(r'sqlite:///'+dbfile)
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # Base.metadata.create_all(engine)  # create table

    # test(session)

    db = DataBase(dbfile)

    # t = db.session.query(Tag).all()
    # print(t)
    # u = db.session.query(User).all()
    # print(u)
    # s = db.session.query(Source).all()
    # print(s)

    a1 = {'timestamp':func.now(),'title':'hgaeh','tag':'历史','user':'a','link':'sgese','source':'wx'}
    db.insert_article(a1)

    # a = db.query_userarticle_bytitle('xx','测试')
    # print(a[0].link)

    # a = db.session.query(Tag).all()
    # print(a)

    u = db.session.query(User).filter_by(name='a').first()
    for a in u.articles:
        # if a.tag.name == '笑话' and 't' in a.title:
        print(a)