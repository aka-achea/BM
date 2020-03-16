
__version__ = 20200315

import configparser


confile = r'M:\MyProject\BM\bm.ini'
config = configparser.ConfigParser()
config.read(confile)
mailsvr = config['mailsvr']['pop']
user = config['mailsvr']['user']
key = config['mailsvr']['key']
dbfile = config['setting']['dbfile']
logfile = config['setting']['log']
attention = config['setting']['attention']
ffile = config['setting']['ff']
