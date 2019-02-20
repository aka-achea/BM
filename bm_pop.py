#!/usr/bin/python
#coding:utf-8
#Python3

import wget

import poplib,configparser,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate,parsedate_to_datetime

# customized module
from mylog import get_funcname, mylogger

confile = r'M:\MyProject\BM\bm.ini'
config = configparser.ConfigParser()
config.read(confile)
mailsvr = config['mailsvr']['pop']
user = config['mailsvr']['user']
key = config['mailsvr']['key']
dbfile = config['setting']['dbfile']
logfilelevel = int(config['setting']['logfilelevel'])
logfile = config['setting']['log']
attention = config['setting']['attention']


def guess_charset(msg):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        l.debug(content_type)
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    l.debug('Message body charset: '+charset)
    return charset

def decode_str(s):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    value, charset = decode_header(s)[0]
    if charset:
        l.debug('Header charset: '+charset)
        value = value.decode(charset)
    l.debug(value)
    return value

def read_mail(msg, indent=0):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    f = {} # mail,tag,date,link
    if indent == 0:
        for header in ['From','To','Subject','Date']:
            value = msg.get(header, '')            
            if value:                
                if header == 'From':
                    l.debug('Look for FROM address')
                    hdr, addr = parseaddr(value)
                    l.debug(addr)
                    f['mail']=addr
                elif header=='Subject':
                    l.debug('Look for TAG')
                    value = decode_str(value)
                    tag = value[:1]
                    l.debug('Tag: '+tag)
                    f['tag']=tag
                elif header == 'Date':
                    l.debug('Look for DATE')
                    mdate = time.strftime('%Y-%m-%d %H:%M:%S',parsedate(value))
                    l.debug(mdate)
                    f['date'] = mdate
                else:
                    l.debug('Header: '+value)

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            l.info('%spart %s' % ('  ' * indent, n))
            l.info('%s-------' % ('  ' * indent))
            read_mail(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        l.debug('Message body content type: '+content_type)
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            l.debug('Content is')
            l.debug(content)
            charset = guess_charset(msg)            
            if charset:
                content = content.decode(charset)
            l.debug('Content after decode')
            l.debug(content)
            # link = content.split('\r\n')[0]
            content = content.split('\r\n')
            l.debug(content)
            for h in content:
                if h[:4] == 'http':
                    f['link'] = h        
            #what if multiple http link?
        else:
            l.info('%sAttachment: %s' % ('  ' * indent, content_type))
    l.debug('Favor entry: '+str(f))
    return f # mail,tag,date,link
    
def get_fav():
    l = mylogger(logfile,logfilelevel,get_funcname())    
    try:
        M = poplib.POP3_SSL(mailsvr)
    except TimeoutError as e:
        l.error(e)
        l.error('Retry')
    # M.set_debuglevel(2)
    l.debug(M.getwelcome())
    # M.apop(user,key) # not supported
    M.user(user)
    M.pass_(key)
    MS = M.stat()
    l.debug(MS)
    ff = {}
    num = len(M.list()[1])
    l.info("You have %d messages." % num)

    for i in range(int(num),0,-1):
        resp, lines, octets = M.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        # l.debug(msg)
        f = read_mail(msg)
        if 'link' in f.keys():
            ff[i]=f
            M.dele(i)
            l.debug('Remove email')
        else:
            ff[i]=f
            l.error('Empty link Email from: '+f['mail'])
        
    l.debug('Favor list: '+str(ff))
    M.quit()
    return ff # favor list without title

if __name__ == "__main__":
    ff = get_fav()
    print(ff)