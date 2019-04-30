#!/usr/bin/python3
#coding:utf-8
#tested in win


import sqlite3 , sys
from prettytable import PrettyTable , from_db_cursor

# customized module
from mylog import get_funcname, mylogger
from bm_pop import logfile,dbfile


class db():  
    def create(self):

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
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()    
        ml.debug(adic)    
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
            ml.error(e)
            ml.error('duplicate entry')
        cursor.close()
        conn.commit()
        conn.close()

    # def q_tag(self,dbfile,tag):
    #     conn = sqlite3.connect(dbfile)
    #     cursor = conn.cursor()        
    #     cmd = 'select title,link from bookmark where tag = "'+tag+'"'
    #     print(cmd)
    #     cursor.execute(cmd)
    #     v = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return v

    # def q_source(self,dbfile,source):
    #     conn = sqlite3.connect(dbfile)
    #     cursor = conn.cursor()        
    #     cursor.execute('select title,link from bookmark')
    #     v = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return v

    # def q_keyword(self,dbfile,keyword):
    #     conn = sqlite3.connect(dbfile)
    #     cursor = conn.cursor() 
    #     cmd = 'select title,link from bookmark where title like "%'+keyword+'%"'
    #     print(cmd)       
    #     cursor.execute(cmd)
    #     v = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return v  

    # def q_t(self,dbfile,keyword):
    #     conn = sqlite3.connect(dbfile)
    #     cursor = conn.cursor() 
    #     cmd = 'select title,link from bookmark where title like "%'+keyword+'%"'
    #     print(cmd)       
    #     cursor.execute(cmd)
    #     v = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return v  

    # def q_a(self,dbfile):
    #     l = mylogger(logfile,get_funcname()) 
    #     conn = sqlite3.connect(dbfile)
    #     cursor = conn.cursor() 
    #     cmd = 'select * from bookmark order by title'
    #     l.debug(cmd)       
    #     cursor.execute(cmd)
    #     # v = cursor.fetchall()
    #     v = from_db_cursor(cursor)
    #     v.align['title']='l'
    #     cursor.close()
    #     conn.close()
    #     return v  

    def query(self,q='',keyword=''):
        ml = mylogger(logfile,get_funcname()) 
        if q in ['title','link','source','tag','mail','mail','date']:
            cmd = 'select * from bookmark where '+q+' like "%'+keyword+'%" order by title' 
        elif keyword =='' and q =='':
            cmd = 'select * from bookmark'
        else:
            ml.error('Missing keyword')
            sys.exit()
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()  
        ml.debug(cmd)
        cursor.execute(cmd)
        num = len(cursor.fetchall())
        ml.debug(num)
        if num == 0:
            ml.debug('No Entry find')
            return False
        cursor.execute(cmd) # need to improve
        v = from_db_cursor(cursor)
        v.align['title']='l'
        cursor.close()
        conn.close()
        return v  



    def d_title(self,keyword):
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor() 
        cmd = 'delete from bookmark where title like "%'+keyword+'%"'
        ml.debug(cmd)       
        cursor.execute(cmd)
        cursor.close()
        conn.close()

    def u_tag(self,ntag,title):    
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor() 
        cmd = 'update bookmark set tag = "'+ntag+'" where title like "%'+keyword+'%"'
        ml.debug(cmd)       
        cursor.execute(cmd)
        cursor.close()
        conn.close()

if __name__=='__main__':
    db = db()
    # db.create(dbfile)
    v = db.query()
    # print(v)
    ml = mylogger(logfile,get_funcname()) 
    ml.info(v.get_string(fields = ['title','time','tag','link']))

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

   