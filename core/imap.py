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

import ssl
from imapclient import IMAPClient

HOST = 'imap.163.com'

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# context manager ensures the session is cleaned up
with IMAPClient(host=HOST,ssl_context=ssl_context) as client:
    client.login(user,key)
    client.select_folder('INBOX')

    # search criteria are passed in a straightforward way
    # (nesting is supported)
    messages = client.search(['NOT', 'DELETED'])

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    for message_id, data in response.items():
        print('{id}: {size} bytes, flags={flags}'.format(
            id=message_id,
            size=data[b'RFC822.SIZE'],
            flags=data[b'FLAGS']))