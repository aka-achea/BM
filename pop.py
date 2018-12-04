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
    l.info(charset)
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        l.info(content_type)
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    funcname = 'note.decode_str'    
    l = ml.mylogger(logfile,logfilelevel,funcname)
    value, charset = decode_header(s)[0]
    l.info(charset)
    if charset:
        value = value.decode(charset)
    l.info(value)
    return value

def print_info(msg, indent=0):
    funcname = 'note.print_info'    
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            l.info(value)
            if value:
                if header == 'From':
                    hdr, addr = parseaddr(value)
                    l.warning(addr)


                # if header=='Subject':
                #     l.info(header)
                #     value = decode_str(value)
                #     l.info(value)
                # else:
                #     hdr, addr = parseaddr(value)
                #     name = decode_str(hdr)
                #     value = u'%s <%s>' % (name, addr)
            # l.info('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            l.info('%spart %s' % ('  ' * indent, n))
            l.info('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        l.info(content_type)
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            l.info(content)
            charset = guess_charset(msg)
            l.info(charset)
            if charset:
                content = content.decode(charset)
            l.info('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            l.info('%sAttachment: %s' % ('  ' * indent, content_type))


def getmail():
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
    # resp, mails, octets = M.list()
    # print(mails)

    #Get the number of mail messages
    numMessages = len(M.list()[1])

    l.info("You have %d messages." % numMessages)

    newest = MS[0]
    # print("Message List:")

    head = M.top(newest,0)[1]
    # print(head)
    resp, lines, octets = M.retr(newest)
    # print(message)
    # body = [line for line in message[1] if line not in head[1]] 

    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)

    print_info(msg)

    # print(a)
    # #List the subject line of each message
    # for mList in range(numMessages) :
    #     for msg in M.retr(mList+1)[1]:
    #         if msg.startswith('Subject'):
    #             print('\t' + msg)
    #             break

    # M.quit()

if __name__ == "__main__":
    getmail()