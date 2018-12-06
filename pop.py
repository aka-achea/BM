#!/usr/bin/python
#coding:utf-8
#Python3


import poplib,configparser
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\BM.log'



def guess_charset(msg):
    funcname = 'note.guess_charset'    
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
    funcname = 'note.decode_str'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    value, charset = decode_header(s)[0]
    l.debug(charset)
    if charset:
        value = value.decode(charset)
    l.debug(value)
    return value

def read_mail(msg, indent=0):
    funcname = 'note.print_info'    
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    f = {}
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')            
            if value:
                l.debug(value)
                if header == 'From':
                    hdr, addr = parseaddr(value)
                    l.debug(addr)
                    f['mail']=addr
                if header=='Subject':
                    l.debug(header)
                    value = decode_str(value)
                    l.debug(value)
                    tag = value[:1]
                    l.debug(tag)
                    f['tag']=tag
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
            l.debug(content)
            link = content.split('\r\n')[0]
            if link[:4] == 'http':
                f['link']=link
            else:
                l.error('Cannot find link')
        else:
            l.info('%sAttachment: %s' % ('  ' * indent, content_type))
    return f
    


def get_fav():
    funcname = 'note.getmail'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    confile = 'E:\\pop.ini'
    config = configparser.ConfigParser()
    config.read(confile)

    mailsvr = config['mailsvr']['mailsvr']
    user = config['user']['user']
    key = config['key']['key']

    M = poplib.POP3_SSL(mailsvr)
    # M.set_debuglevel(2)
    l.debug(M.getwelcome())
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
        f = read_mail(msg)
        l.debug(f)
        ff[i]=f
    l.debug(ff)

    M.quit()
    return ff

if __name__ == "__main__":
    ff = get_fav()
    print(ff)