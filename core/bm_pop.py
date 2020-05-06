#!/usr/bin/python3
#coding:utf-8
#tested in Win

import poplib,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate,parsedate_to_datetime

# customized module
from mylog import get_funcname, mylogger
from config import mailsvr,user,key,logfile


def guess_charset(msg):
    ml = mylogger(logfile,get_funcname()) 
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        ml.dbg(content_type)
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    ml.dbg('Message body charset: '+charset)
    return charset


def decode_str(s):
    ml = mylogger(logfile,get_funcname()) 
    value, charset = decode_header(s)[0]
    if charset:
        ml.dbg('Header charset: '+charset)
        value = value.decode(charset)
    ml.dbg(value)
    return value


def read_mail(msg, indent=0):
    '''Main function to read mail message'''
    ml = mylogger(logfile,get_funcname()) 
    f = {} # mail,tag,date,link
    if indent == 0:
        for header in ['From','To','Subject','Date']:
            value = msg.get(header, '')            
            if value:                
                if header == 'From':
                    hdr, addr = parseaddr(value)
                    ml.dbg(f'Find FROM address {addr}')
                    f['email']=addr
                elif header=='Subject':
                    ml.dbg('Look for TAG')
                    value = decode_str(value)
                    tag = value[:1]
                    ml.dbg('Tag: '+tag)
                    f['tag']=tag.lower()
                elif header == 'Date':
                    ml.dbg('Look for DATE')
                    mdate = time.strftime('%Y-%m-%d %H:%M:%S',parsedate(value))
                    ml.dbg(mdate)
                    f['timestamp'] = mdate
                else:
                    ml.dbg('Header: '+value)

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            ml.dbg('%spart %s' % ('  ' * indent, n))
            ml.dbg('%s-------' % ('  ' * indent))
            read_mail(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        ml.dbg('Message body content type: '+content_type)
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            ml.dbg('Content is')
            ml.dbg(content)
            charset = guess_charset(msg)            
            if charset:
                content = content.decode(charset)
            ml.dbg('Content after decode')
            # ml.dbg(content)
            # link = content.split('\r\n')[0]
            content = content.split('\r\n')
            ml.dbg(content)
            for h in content:
                if h[:4] == 'http':
                    f['link'] = h        
            #what if multiple http link?
        else:
            ml.dbg('%sAttachment: %s' % ('  ' * indent, content_type))
    ml.dbg('Favor entry: '+str(f))
    return f # mail,tag,date,link
    
def get_fav() -> list:
    '''Emurate favorite from email'''
    ml = mylogger(logfile,get_funcname()) 
    try:
        M = poplib.POP3_SSL(mailsvr)
    except TimeoutError as e:
        ml.err(e)
        ml.err('Retry')
    # M.set_debuglevel(2)
    ml.dbg(M.getwelcome())
    # M.apop(user,key) # not supported
    M.user(user)
    M.pass_(key)
    MS = M.stat()
    ml.dbg(MS)
    ff = {}
    num = len(M.list()[1])
    ml.info("You have %d messages." % num)
    for i in range(int(num),0,-1):
        resp, lines, octets = M.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        # ml.info(msg)
        f = read_mail(msg)
        if 'link' in f.keys():
            ff[i]=f
            M.dele(i)
            ml.info('Remove email')
        else:
            ff[i]=f
            ml.err('Empty link Email from: '+f['email'])
        
    ml.dbg('Favor list: '+str(ff))
    M.quit()
    return ff # favor list without title

if __name__ == "__main__":
    ff = get_fav()
    print(ff)