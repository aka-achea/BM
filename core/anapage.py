#!/usr/bin/python3
#coding:utf-8
#tested in win

__version__ = 20200315

from bs4 import BeautifulSoup
import re
from functools import lru_cache

# customized module
# from modstr import modificate
from openlink import op_simple,ran_header
from config import logfile
from mylog import get_funcname,mylogger


@lru_cache(maxsize=32)
def ana_wx(page):
    '''Analyze Weixin web'''
    ml = mylogger(logfile,get_funcname())   
    html = op_simple(page,ran_header())[0]
    # print(html)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    # bsObj = BeautifulSoup(html,"html5lib") #;print(bsObj)
    try:
        author = bsObj.find('span',{'class':'rich_media_meta rich_media_meta_nickname'})
        author = author.a.text.strip()
        title = bsObj.find('h2',{'class':'rich_media_title'})
        title = title.text.strip()
        p = {'author':author,'title':title}
        # p['link'] = page
        ml.dbg(p)
    except:
        return None
    return p


@lru_cache(maxsize=32)
def ana_mono(page): 
    '''Analyze Mono web'''
    ml = mylogger(logfile,get_funcname())   
    html = op_simple(page,ran_header())[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    author = bsObj.find('span',{'class':'title'}).text.strip()
    title = bsObj.find('h1',{'class':'title'}).text.strip()
    p = {'author':author,'title':title}
    ml.debug(p)
    return p


@lru_cache(maxsize=32)
def ana_dy(page): 
    '''Analyze Douyin web'''
    ml = mylogger(logfile,get_funcname())   
    html = op_simple(page,ran_header())[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    author = bsObj.find('p',{'class':'name nowrap'}).text.strip()
    title = bsObj.find('h1',{'class':'desc'}).text.strip()
    p = {'author':author,'title':title}
    ml.info(p)
    return p


if __name__ == "__main__":
    page = 'https://v.douyin.com/7uCmaC/'
    print(ana_dy(page))