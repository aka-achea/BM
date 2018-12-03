#!/usr/bin/python
#coding:utf-8
#Python3


import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


M = poplib.POP3_SSL('pop.163.com')
# M.set_debuglevel(2)
# print(M.getwelcome())
M.user('@163.com')
M.pass_('')

MS = M.stat()
print(MS)

# resp, mails, octets = M.list()
# print(mails)

#Get the number of mail messages
numMessages = len(M.list()[1])

print("You have %d messages." % numMessages)

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