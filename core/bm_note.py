#!/usr/bin/python3
#coding:utf-8
#tested in win

__version__ = 20200315

import time
import os
import json
from bs4 import BeautifulSoup
# from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from pprint import pprint

# customized module
# from modstr import modificate
from openlink import op_simple,ran_header
from notedb import NoteDataBase
from bm_pop import get_fav
from config import logfile,dbfile,attention,ffile
from mylog import get_funcname,mylogger
from anapage import ana_wx,ana_mono

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
    ml = mylogger(logfile,get_funcname())  


    if os.path.exists(ffile):
        with open(ffile,'r',encoding='utf-8') as f:
            ff = json.loads(f.read())
    else:
        ml.info('Query Email')
        ff = get_fav()
        with open(ffile,'w',encoding='utf-8') as x:
            json.dump(ff,x,ensure_ascii=False,indent=2)
    # fl = {}  # favor list
    db = NoteDataBase(dbfile)   
    pprint(ff)
    for x in range(1,len(ff)+1):
        f = ff[str(x)] #email,tag,timestamp,link
        ml.dbg(f)
        if 'link' in f.keys():     
            link = f['link']
            if link.split('/')[2] == 'mp.weixin.qq.com':
                p = ana_wx(link)
                if p:                
                    f['source'] = '微信公众号'
                    f['author'] = p['author']
                    f['title'] = p['title']  
                    ml.dbg(f)
                else:
                    with open(attention,'a') as f:                
                        f.write('Need to check: '+link+'\n')
                    continue
            elif link.split('/')[2] == 'mmmono.com':
                if p := ana_mono(link):
                    f['source'] = 'MONO'
                    f['author'] = p['author']
                    f['title'] = p['title']  
                    ml.dbg(f)
                else:
                    with open(attention,'a') as f:                
                        f.write('Need to check: '+link+'\n')
                    continue
            elif link.split('/')[2] == 'v.douyin.com':
                pass
            else:
                ml.warn('Need to check source')
                raise
                # fl[i] = f
            db.insert_article(f) #email,tag,timestamp,link,source,author,title
        else:
            ml.info('Empty link Email from: '+f['email'])
            b = f['email']
            with open(attention,'a') as f:                
                f.write('Empty link Email from: '+b+'\n')
            # fl[i] = f





if __name__=='__main__':
    # ff = {1: {'mail': 'CJYRB@hotmail.com', 'tag': '计', 'date': '2018-12-07 11:39:48', 'link': 'https://mp.weixin.qq.com/s/vwF0QOkz4if47FZ9x0t3NA'},2: {'mail': 'CJYRB@hotmail.com', 'tag': '食', 'date': '2018-12-05 09:57:23', 'link': 'https://mp.weixin.qq.com/s/A1YL4oVkdXvsdGAx0-2mIw'}}
    main()


    # page = 'file:///E://0.html'


    # tag = 'test'
    # mail = 't@ge.com'
    # p = ana_wx(page)
    # a = create_note(page,tag,mail)

  