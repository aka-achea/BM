#!/usr/bin/python
#coding:utf-8
# Python3

import sqlite3,sys
from prettytable import PrettyTable , from_db_cursor

import mylog as ml
logfilelevel = 10 # Debug
logfile = r'M:\MyProject\BM\BM.log'
dbfile = r'M:\MyProject\BM\bm.db'

class db():
    def __init__(self):
        self.dbfile = dbfile

    def create(self,dbfile):

        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('create table bookmark (\
                        time varchar(100) primary key,\
                        title varchar(100),\
                        tag varchar(20),\
                        author varchar(50),\
                        source varchar(100),\
                        link varchar(1000),\
                        mail varchar(100)   )' 
                        )
        cursor.close()
        conn.close()

    def insert(self,adic):
        funcname = 'db.insert'    
        l = ml.mylogger(logfile,logfilelevel,funcname) 

        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor()    
        l.debug(adic)    
        time = adic['date']
        title = adic['title']
        tag = adic['tag']
        source = adic['source']
        author = adic['author']
        link = adic['link']
        mail = adic['mail']
        try:
            cursor.execute("insert into bookmark values (?,?,?,?,?,?,?)",(time,title,tag,author,source,link,mail))
        except sqlite3.IntegrityError as e:
            l.error(e)
            l.error('duplicate entry')
        cursor.close()
        conn.commit()
        conn.close()

    def query(self,keyword='',q=''):
        funcname = 'db.query'    
        l = ml.mylogger(logfile,logfilelevel,funcname) 
        if q in ['title','tag','source','author','mail','time']:
            cmd = 'select title,link from bookmark where '+q+' like "%'+keyword+'%" order by title' 
        elif keyword =='' and q =='':
            cmd = 'select title,link from bookmark'
        else:
            l.error('Missing keyword')
            sys.exit()
        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor()  
        cursor.execute(cmd)
        v = from_db_cursor(cursor)
        v.align['title']='l'
        cursor.close()
        conn.close()
        return v  

    def d_title(self,dbfile,keyword):
        funcname = 'db.d_title'    
        l = ml.mylogger(logfile,logfilelevel,funcname) 
        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor() 
        cmd = 'delete from bookmark where title like "%'+keyword+'%"'
        l.debug(cmd)       
        cursor.execute(cmd)
        cursor.close()
        conn.close()

    def u_tag(self,dbfile,ntag,title):
        funcname = 'db.d_title'    
        l = ml.mylogger(logfile,logfilelevel,funcname) 
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor() 
        cmd = 'update bookmark set tag = "'+ntag+'" where title like "%'+title+'%"'
        l.debug(cmd)       
        cursor.execute(cmd)
        cursor.close()
        conn.close()

if __name__=='__main__':
    db = db()
    # db.create(dbfile)

    v = db.query()
    # print(v)
    print(v.get_string(fields = ['title','time','tag','link']))

    # adic = { 'tag': 'test',\
    #      'link': 'https://mp.weixin.qq.com/s/-O2wEBNQmj1MoTC1fnwECg', 'title':\
    #      '真正的移动开发者，该如何直面App的崩溃率', 'source': 'InfoQ','mail':'a@14.com'}
    # t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # adic['time'] = t
    # # print(adic)
    # tag = adic['tag']
    # db.insert(adic,dbfile)
    # v= db.query(dbfile,tag)
            # for i in v: print(i)
    # keyword = '流水线'
    # v = db.q_keyword(dbfile,keyword)
    # for i in v: print(i)

    # tag = '畅'
    # v = db.q_tag(dbfile,tag)
    # for i in v: print(i)

    # source = '果壳'

   