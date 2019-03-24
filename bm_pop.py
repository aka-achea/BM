#!/usr/bin/python3
#coding:utf-8
#tested in Win

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
logfile = config['setting']['log']
attention = config['setting']['attention']


def guess_charset(msg):
    ml = mylogger(logfile,get_funcname()) 
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        ml.debug(content_type)
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    ml.debug('Message body charset: '+charset)
    return charset

def decode_str(s):
    ml = mylogger(logfile,get_funcname()) 
    value, charset = decode_header(s)[0]
    if charset:
        ml.debug('Header charset: '+charset)
        value = value.decode(charset)
    ml.debug(value)
    return value

def read_mail(msg, indent=0):
    ml = mylogger(logfile,get_funcname()) 
    f = {} # mail,tag,date,link
    if indent == 0:
        for header in ['From','To','Subject','Date']:
            value = msg.get(header, '')            
            if value:                
                if header == 'From':
                    ml.debug('Look for FROM address')
                    hdr, addr = parseaddr(value)
                    ml.debug(addr)
                    f['mail']=addr
                elif header=='Subject':
                    ml.debug('Look for TAG')
                    value = decode_str(value)
                    tag = value[:1]
                    ml.debug('Tag: '+tag)
                    f['tag']=tag
                elif header == 'Date':
                    ml.debug('Look for DATE')
                    mdate = time.strftime('%Y-%m-%d %H:%M:%S',parsedate(value))
                    ml.debug(mdate)
                    f['date'] = mdate
                else:
                    ml.debug('Header: '+value)

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            ml.info('%spart %s' % ('  ' * indent, n))
            ml.info('%s-------' % ('  ' * indent))
            read_mail(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        ml.debug('Message body content type: '+content_type)
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            ml.debug('Content is')
            ml.debug(content)
            charset = guess_charset(msg)            
            if charset:
                content = content.decode(charset)
            ml.debug('Content after decode')
            ml.debug(content)
            # link = content.split('\r\n')[0]
            content = content.split('\r\n')
            ml.debug(content)
            for h in content:
                if h[:4] == 'http':
                    f['link'] = h        
            #what if multiple http link?
        else:
            ml.info('%sAttachment: %s' % ('  ' * indent, content_type))
    ml.debug('Favor entry: '+str(f))
    return f # mail,tag,date,link
    
def get_fav():
    ml = mylogger(logfile,get_funcname())    
    try:
        M = poplib.POP3_SSL(mailsvr)
    except TimeoutError as e:
        ml.error(e)
        ml.error('Retry')
    # M.set_debuglevel(2)
    ml.debug(M.getwelcome())
    # M.apop(user,key) # not supported
    M.user(user)
    M.pass_(key)
    MS = M.stat()
    ml.debug(MS)
    ff = {}
    num = len(M.list()[1])
    ml.info("You have %d messages." % num)

    for i in range(int(num),0,-1):
        resp, lines, octets = M.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        # ml.debug(msg)
        f = read_mail(msg)
        if 'link' in f.keys():
            ff[i]=f
            M.dele(i)
            ml.debug('Remove email')
        else:
            ff[i]=f
            ml.error('Empty link Email from: '+f['mail'])
        
    ml.debug('Favor list: '+str(ff))
    M.quit()
    return ff # favor list without title

if __name__ == "__main__":
    ff = get_fav()
    print(ff)