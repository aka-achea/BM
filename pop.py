#!/usr/bin/python
#coding:utf-8
#Python3


import poplib,configparser,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate,parsedate_to_datetime

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\BM.log'



def guess_charset(msg):
    funcname = 'pop.guess_charset'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    charset = msg.get_charset()
    l.debug(charset)
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        l.debug(content_type)
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    funcname = 'pop.decode_str'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    value, charset = decode_header(s)[0]
    l.debug(charset)
    if charset:
        value = value.decode(charset)
    l.debug(value)
    return value

def read_mail(msg, indent=0):
    funcname = 'pop.read_mail'    
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    f = {} # mail,tag,date,link
    if indent == 0:
        for header in ['From', 'To', 'Subject','Date']:
            value = msg.get(header, '')  
            l.debug(value)          
            if value:                
                if header == 'From':
                    l.debug('Look for From address')
                    hdr, addr = parseaddr(value)
                    l.debug(addr)
                    f['mail']=addr
                if header=='Subject':
                    l.debug('Look for Subject')
                    value = decode_str(value)
                    l.debug(value)
                    tag = value[:1]
                    l.debug(tag)
                    f['tag']=tag
                if header == 'Date':
                    l.debug('Look for Date')
                    mdate = time.strftime('%Y-%m-%d %H:%M:%S',parsedate(value))
                    l.debug(mdate)
                    f['date'] = mdate
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            l.info('%spart %s' % ('  ' * indent, n))
            l.info('%s-------' % ('  ' * indent))
            read_mail(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        l.debug(content_type)
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            l.debug(content)
            charset = guess_charset(msg)            
            if charset:
                l.debug(charset)
                content = content.decode(charset)
            # l.debug(content)
            # link = content.split('\r\n')[0]

            content = content.split('\r\n')
            # l.debug(content)
            for h in content:
                if h[:4] == 'http':
                    f['link'] = h        

        else:
            l.info('%sAttachment: %s' % ('  ' * indent, content_type))
    return f
    

def get_fav():
    funcname = 'pop.get_fav'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    confile = 'E:\\bm.ini'
    config = configparser.ConfigParser()
    config.read(confile)

    mailsvr = config['mailsvr']['pop']
    user = config['user']['user']
    key = config['key']['key']
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
        l.debug(f)
        if 'link' in f.keys():
            ff[i]=f
            M.dele(i)
            l.debug('Remove email')
        else:
            ff[i]=f
            l.error('Empty link Email from: '+f['mail'])
        
    l.debug(ff)
    M.quit()
    return ff

if __name__ == "__main__":
    ff = get_fav()
    print(ff)