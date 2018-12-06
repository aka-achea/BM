#!/usr/bin/python
#coding:utf-8
#Python3

import time
from bs4 import BeautifulSoup
# from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser

# customized module
# from modstr import modificate
from openlink import op_simple

from store import db
from pop import get_fav 

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'



def ana_wx(page):
    funcname = 'note.ana_wx'
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    html = op_simple(page)[0]
    # print(html)
    # html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    # bsObj = BeautifulSoup(html,"html5lib") #;print(bsObj)

    source = bsObj.find('span',{'class':'rich_media_meta rich_media_meta_nickname'})
    source = source.a.text.strip()

    title = bsObj.find('h2',{'class':'rich_media_title'})
    title = title.text.strip()

    p = {'source':source,'title':title}
    # p['link'] = page
    l.debug(p)

    return p


def create_note(page,tag,mail): # return bookmark dictionary
    a = {}
    t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    a['time'] = t
    a['tag'] = tag
    a['source'] = p['gzh']
    a['title'] = p['title']
    a['link'] = p['link']
    a['mail'] = mail
    print(a)
    return a

def main():
    funcname = 'note.main'
    l = ml.mylogger(logfile,logfilelevel,funcname)  
    # ff = get_fav()
    ff = {2: {'mail': 'CJYRB@hotmail.com', 'tag': 'F', 'link': 'https://mp.weixin.qq.com/s/A1YL4oVkdXvsdGAx0-2mIw'}, 1: {'mail': 'CJYRB@hotmail.com', 'tag': '畅', 'link': 'https://mp.weixin.qq.com/s/PRarJI24Y8YxmmSm_l6-IA'}}
    l.debug(ff)
    fl = {}
    num = len(ff)+1    
    for i in range(1,num):
        f = ff[i]
        link = f['link']
        p = ana_wx(link)
        f['source'] = p['source']
        f['title'] = p['title']
        l.info(f)
        fl[i] = f
    
    print(fl)

    dbfile = 'E:\\bm.db'
    d = db()
    num = len(fl)+1    
    for i in range(1,num):
        t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f = fl[i] 
        f['time'] = t
        d.insert(f,dbfile)

  

    # db.insert(a,dbfile)
    # v= db.q_tag(dbfile,tag)
    # for i in v: print(i)
    source = 'InfoQ'
    v = d.q_source(dbfile,source)
    for i in v: print(i)





if __name__=='__main__':
    main()
    # page = 'https://mp.weixin.qq.com/s/-O2wEBNQmj1MoTC1fnwECg'
    # page = 'file:///E://0.html'


    # tag = 'test'
    # mail = 't@ge.com'
    # p = ana_wx(page)
    # a = create_note(page,tag,mail)

  