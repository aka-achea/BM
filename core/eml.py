# Import the email modules we'll need
from email.parser import Parser
# from email.policy import default
# from email import message_from_file
import re
import os
import json
import time
from pprint import pprint
from email.header import decode_header
from email.utils import parsedate,parseaddr

# customized module
from mylog import get_funcname, mylogger
from config import logfile,ffile


messagefile = r'D:\Download\m\文汉服，中国人最美的衣服.eml'


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

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

def read_eml(messagefile):
    f = {} # mail,tag,date,link
    # If the e-mail headers are in a file, uncomment these two lines:
    with open(messagefile, 'r') as fp:
        email = fp.read()
        emailcontent = Parser().parsestr(email)	#经过parsestr处理过后生成一个字典
        # for k,v in emailcontent.items():
        #     print(k)
        To = parseaddr(emailcontent['To'])[1]
        f['email'] = parseaddr(emailcontent['From'])[1]
        subject = decode_str(emailcontent['Subject'])
        f['tag'] = subject[:1].lower()
        Date = emailcontent['Date']
        f['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S',parsedate(Date))
        # 循环信件中的每一个mime的数据块
        for par in emailcontent.walk():
            if not par.is_multipart(): # 这里要判断是否是multipart，是的话，里面的数据是无用的
                content_type = par.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    content = par.get_payload(decode=True)
                    if charset := guess_charset(par):
                        content = content.decode(charset)
                    for h in content.split('\r\n'):
                        if h[:4] == 'http':
                            f['link'] = h     
                    # print(content)
    return f

def read_emlfolder(folder):
    ff = {}
    for n,x in enumerate(os.listdir(folder)):
        messagefile = os.path.join(folder,x)
        # print(n+1,messagefile)
        f = read_eml(messagefile)
        if 'link' in f.keys():
            ff[n+1]=f
    # print(ff)
    with open(ffile,'w',encoding='utf-8') as fp:
        json.dump(ff,fp,ensure_ascii=False,indent=2)

if __name__ == "__main__":
    fd = r'D:\Download\m'
    read_emlfolder(fd)
