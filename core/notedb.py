#!/usr/bin/env python
#coding:utf-8
#tested in win

__version__ = 20200315

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash


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


class NoteDataBase():
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.engine = create_engine(r'sqlite:///'+self.dbfile)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()        

    def reset_db(self):
        import os
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
        Base.metadata.create_all(self.engine)  # create table

    def query_tagid(self,tagname):
        return self.session.query(Tag).filter_by(name=tagname).first().id

    def query_userid_bymail(self,email):
        return self.session.query(User).filter_by(email=email).first().id

    def query_srcid(self,fullname):
        return self.session.query(Source).filter_by(fullname=fullname).first().id

    def query_userarticle_bytitle(self,user,title):
        u = self.session.query(User).filter_by(name=user).first()
        uarticles = []
        for f in u.uarticles:
            if title in f.title:
                uarticles.append(f)
        return uarticles

    def insert_src(self,sourcename,fullname):
        s = Source(name=sourcename,fullname=fullname)
        self.session.add(s)
        self.session.commit()

    def insert_tag(self,tagname,fullname):
        t = Tag(name=tagname,fullname=fullname)
        self.session.add(t)
        self.session.commit()   

    def insert_user(self,email,username,password):
        u = User(email=email,name=username,password=password)
        self.session.add(u)
        self.session.commit()  

    def insert_article(self,article_dict):
        timestamp = article_dict['timestamp']
        title = article_dict['title']
        tagid = self.query_tagid(article_dict['tag'])
        author = article_dict['author']
        # print(article_dict['email'].upper())
        userid = self.query_userid_bymail(article_dict['email'].upper())
        link = article_dict['link']
        src_id = self.query_srcid(article_dict['source'])
        article = Article(timestamp=timestamp,title=title,author=author,tag_id=tagid,
                            user_id=userid,link=link,src_id=src_id)
        self.session.add(article)
        self.session.commit()




if __name__ == "__main__":
    # dbfile = r'E:\UT\note-test.sqlite'
    dbfile = r'M:\MyProject\BM\note-prd.sqlite'
    db = NoteDataBase(dbfile)

    f = {'email': 'CJYRB@hotmail.com', 'tag': '生', 'timestamp': '2019-12-02 02:02:31', 
    'link': 'https://mp.weixin.qq.com/s/uNRU8mbtmFKlAphd_itzyA', 'source': '微信公众号', 
    'author': '申工社', 'title': '太棒了叭！这100个实用生活小妙招懒人必备！许多都万万没想到…'}
    db.insert_article(f)

    # test(session)
    # t = db.session.query(Tag).all()
    # print(t)
    # u = db.session.query(User).all()
    # print(u)
    # s = db.session.query(Source).all()
    # print(s)

    # a1 = {'timestamp':func.now(),'title':'hgaeh','tag':'历史','user':'a','link':'sgese','source':'wx'}
    # db.insert_article(a1)

    # # a = db.query_userarticle_bytitle('xx','测试')
    # # print(a[0].link)

    u = db.session.query(User).filter_by(name='JASON').first()
    for a in u.articles:
        print(a)
    # u.password = 'welcome'
    # u.show_hash()
    # db.session.commit()
    # print(u.verify_password('welcome'))