#!/usr/bin/python3
#coding:utf-8
#tested in Win

import imaplib,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate,parsedate_to_datetime

# customized module
from mylog import get_funcname, mylogger
from config import mailsvr,user,key,logfile


try:
    print(mailsvr)
    M = imaplib.IMAP4_SSL('imap.163.com')
    M.login(user,key)
except TimeoutError as e:
    ml.err(e)
    ml.err('Retry')

M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
M.close()
M.logout()



