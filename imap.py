#!/usr/bin/python
#coding:utf-8
#Python3


import imaplib,configparser,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate,parsedate_to_datetime

# Customized module
import mylog as ml
logfilelevel = 10 # Debug
logfile = r'M:\MyProject\BM\BM.log'



def read_mail(msg, indent=0):
    funcname = 'pop.read_mail'    
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    f = {}
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
                    f['Date'] = mdate
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
            # link = content.split('\r\n')[0]

            content = content.split('\r\n')
            for l in content:
                if l[:4] == 'http':
                    f['link'] = l
            if  f['link'] == '':
                l.error('Cannot find link')
        else:
            l.info('%sAttachment: %s' % ('  ' * indent, content_type))
    return f
    


def get_fav():
    funcname = 'imap.get_fav'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    confile = 'E:\\BM.ini'
    config = configparser.ConfigParser()
    config.read(confile)

    mailsvr = config['mailsvr']['imap']
    user = config['user']['user']
    key = config['key']['key']

    M = imaplib.IMAP4_SSL(mailsvr)
    # M.set_debuglevel(2)
    M.login(user,key)
    l.info(M.list())
    M.select()
    M.select('INBOX')
    t, msgnums = M.search(None, 'ALL')
    # print(t)
    print(msgnums)
    # num = len(msgnums)
    # l.info("You have %d new messages." % num)

    # for i in range(int(num),0,-1):
    #     resp, lines, octets = M.retr(i)
    #     msg_content = b'\r\n'.join(lines).decode('utf-8')
    #     msg = Parser().parsestr(msg_content)
    #     # l.debug(msg)
    #     f = read_mail(msg)
    #     l.debug(f)
    #     ff[i]=f
    # l.debug(ff)
    
    # M.quit()
    # return ff

if __name__ == "__main__":
    get_fav()
