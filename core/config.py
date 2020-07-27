
__version__ = 20200726

import configparser
import os

projectpath = r'N:\MyProject\BM'
confile = os.path.join(projectpath,'bm.ini')
config = configparser.ConfigParser()
config.read(confile)
mailsvr = config['mailsvr']['pop']
user = config['mailsvr']['user']
key = config['mailsvr']['key']
dbfile = os.path.join(projectpath,config['setting']['dbfile'])
logfile = os.path.join(projectpath,config['setting']['log'])
attention = os.path.join(projectpath,config['setting']['attention'])
ffile = os.path.join(projectpath,config['setting']['ff'])
