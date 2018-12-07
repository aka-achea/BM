#!/usr/bin/python
#coding:utf-8
# Python3

import sqlite3


class db():
    def create(self,dbfile):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('create table bookmark (\
                        time varchar(100) primary key,\
                        title varchar(100),\
                        tag varchar(20),\
                        source varchar(100),\
                        link varchar(1000),\
                        mail varchar(100)   )' 
                        )
        cursor.close()
        conn.close()

    def insert(self,adic,dbfile):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()    
        print(adic)    
        time = adic['time']
        title = adic['title']
        tag = adic['tag']
        source = adic['source']
        link = adic['link']
        mail = adic['mail']
        cursor.execute("insert into bookmark values (?,?,?,?,?,?)",(time,title,tag,source,link,mail))
        cursor.close()
        conn.commit()
        conn.close()


    def backup(self,dbfile):
        pass

    def q_tag(self,dbfile,tag):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()        
        cmd = 'select title,link from bookmark where tag = "'+tag+'"'
        print(cmd)
        cursor.execute(cmd)
        v = cursor.fetchall()
        cursor.close()
        conn.close()
        return v

    def q_source(self,dbfile,source):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()        
        cursor.execute('select title,link from bookmark')
        v = cursor.fetchall()
        cursor.close()
        conn.close()
        return v

    def q_keyword(self,dbfile,keyword):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor() 
        cmd = 'select title,link from bookmark where title like "%'+keyword+'%"'
        print(cmd)       
        cursor.execute(cmd)
        v = cursor.fetchall()
        cursor.close()
        conn.close()
        return v  

    def q_t(self,dbfile,keyword):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor() 
        cmd = 'select title,link from bookmark where title like "%'+keyword+'%"'
        print(cmd)       
        cursor.execute(cmd)
        v = cursor.fetchall()
        cursor.close()
        conn.close()
        return v  

    def q_custom(self):
        pass
    

if __name__=='__main__':
    import time
    dbfile = 'E:\\bm.db'
    db = db()
    # db.create(dbfile)

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
    keyword = '流水线'
    v = db.q_keyword(dbfile,keyword)
    for i in v: print(i)

    tag = '畅'
    v = db.q_tag(dbfile,tag)
    for i in v: print(i)

    source = '果壳'