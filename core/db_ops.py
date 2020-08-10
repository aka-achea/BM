#!/usr/bin/env python
#coding:utf-8
#tested in win

__version__ = 20200804

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# customized module
from db_base_model import Tag, Source, User, Article


class NoteDataBase():
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.engine = create_engine(r'sqlite:///'+self.dbfile)
        self.session = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))()
        # DBSession = sessionmaker(bind=self.engine)
        # self.session = DBSession()        

    @contextmanager
    def db_session(self,commit=True):
        session = self.session 
        try:
            yield session
            if commit:
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if session:
                session.close()

    # def reset_db(self):
    #     import os
    #     if os.path.exists(self.dbfile):
    #         os.remove(self.dbfile)
    #     Base.metadata.create_all(self.engine)  # create table

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
        with self.db_session() as session:
            session.add(s)

    def insert_tag(self,tagname,fullname):
        t = Tag(name=tagname,fullname=fullname)
        with self.db_session() as session:
            session.add(t)

    def insert_user(self,email,username,password):
        u = User(email=email,name=username,password=password)
        with self.db_session() as session:
            session.add(u)

    def insert_article(self,article_dict):
        with self.db_session() as session:
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
            session.add(article)




if __name__ == "__main__":
    # dbfile = r'E:\UT\note-test.sqlite'
    dbfile = r'N:\MyProject\BM\note-test.sqlite'
    db = NoteDataBase(dbfile)

    f = {'email': 'CJYRB@hotmail.com', 'tag': '生', 'timestamp': '2019-12-02 02:02:31', 
    'link': 'https://mp.weixin.qq.com/s/uNRU8mbtmFKlAphd_itzyA', 'source': '微信公众号', 
    'author': '申工社', 'title': '太棒人必备！许多都万万没想到…'}
    db.insert_article(f)
    id = db.query_tagid('食')
    print(id)
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

    # u = db.session.query(User).filter_by(name='JASON').first()
    # for a in u.articles:
    #     print(a)
    # u.password = 'welcome'
    # u.show_hash()
    # db.session.commit()
    # print(u.verify_password('welcome'))