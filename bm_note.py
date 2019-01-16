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
from bm_store import db
from bm_pop import get_fav,logfile,logfilelevel,dbfile,attention
from mylog import get_funcname,mylogger


def ana_wx(page):
    l = mylogger(logfile,logfilelevel,get_funcname())   
    html = op_simple(page)[0]
    # print(html)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    # bsObj = BeautifulSoup(html,"html5lib") #;print(bsObj)
    author = bsObj.find('span',{'class':'rich_media_meta rich_media_meta_nickname'})
    author = author.a.text.strip()
    title = bsObj.find('h2',{'class':'rich_media_title'})
    title = title.text.strip()
    p = {'author':author,'title':title}
    # p['link'] = page
    l.debug(p)
    return p


def ana_mono(page):
    pass

# def create_note(page,tag,mail): # return bookmark dictionary
#     a = {}
#     t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#     a['time'] = t
#     a['tag'] = tag
#     a['source'] = p['gzh']
#     a['title'] = p['title']
#     a['link'] = p['link']
#     a['mail'] = mail
#     print(a)
#     return a

def main():
    l = mylogger(logfile,logfilelevel,get_funcname())  
    l.debug('Query Email')
    ff = get_fav()
    fl = {}  # favor list
    num = len(ff)+1    
    for i in range(1,num):
        f = ff[i]
        if 'link' in f.keys():     
            link = f['link']
            if link.split('/')[2] == 'mp.weixin.qq.com':
                p = ana_wx(link)
                f['source'] = '微信公众号'
                f['author'] = p['author']
                f['title'] = p['title']  
                l.debug(f)
                fl[i] = f
            else:
                l.warning('Need to check source')
                fl[i] = f
        else:
            # l.debug('Empty link Email from: '+f['mail'])
            fl[i] = f

    l.debug('Full list: '+str(fl))
    l.debug('store in DB')
    d = db()
    num = len(fl)+1    
    for i in range(1,num):        
        f = fl[i]     
        if 'link' in f.keys():     
            d.insert(f)
        else:
            l.debug('Empty link Email from: '+f['mail'])
            b = f['mail']
            with open(attention,'a') as f:                
                f.write('Empty link Email from: '+b+'\n')



if __name__=='__main__':
    # ff = {1: {'mail': 'CJYRB@hotmail.com', 'tag': '计', 'date': '2018-12-07 11:39:48', 'link': 'https://mp.weixin.qq.com/s/vwF0QOkz4if47FZ9x0t3NA'},2: {'mail': 'CJYRB@hotmail.com', 'tag': '食', 'date': '2018-12-05 09:57:23', 'link': 'https://mp.weixin.qq.com/s/A1YL4oVkdXvsdGAx0-2mIw'}}
    main()

    # page = 'https://mp.weixin.qq.com/s/-O2wEBNQmj1MoTC1fnwECg'
    # page = 'file:///E://0.html'


    # tag = 'test'
    # mail = 't@ge.com'
    # p = ana_wx(page)
    # a = create_note(page,tag,mail)

  