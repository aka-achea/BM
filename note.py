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

import store

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'





def ana_wx(page):
    funcname = 'note.ana_wx'
    # l = ml.mylogger(logfile,logfilelevel,funcname)   
    html = op_simple(page)[0]
    # print(html)
    # html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    # bsObj = BeautifulSoup(html,"html5lib") #;print(bsObj)

    gzh = bsObj.find('span',{'class':'rich_media_meta rich_media_meta_nickname'})
    gzh = gzh.a.text.strip()

    title = bsObj.find('h2',{'class':'rich_media_title'})
    title = title.text.strip()

    p = {'gzh':gzh,'title':title}
    p['link'] = page
    # print(p)

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





if __name__=='__main__':
    page = 'https://mp.weixin.qq.com/s/-O2wEBNQmj1MoTC1fnwECg'
    # page = 'file:///E://0.html'
    tag = 'test'
    mail = 't@ge.com'
    p = ana_wx(page)
    a = create_note(page,tag,mail)

    dbfile = 'E:\\bm.db'
    db = store.db()
    tag = a['tag']
    db.insert(a,dbfile)
    v= db.q_tag(dbfile,tag)
    for i in v: print(i)
    source = 'InfoQ'
    v = db.q_source(dbfile,source)
    for i in v: print(i)
