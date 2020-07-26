
__version__ = 20200726

import configparser
import os

projectpath = r'N:\MyProject\BM'
confile = os.path.join(projectpath,'bm.ini')
config = configparser.ConfigParser()
config.read(confile)
mailsvr = os.path.join(projectpath,config['mailsvr']['pop'])
user = os.path.join(projectpath,config['mailsvr']['user'])
key = os.path.join(projectpath,config['mailsvr']['key'])
dbfile = os.path.join(projectpath,config['setting']['dbfile'])
logfile = os.path.join(projectpath,config['setting']['log'])
attention = os.path.join(projectpath,config['setting']['attention'])
ffile = os.path.join(projectpath,config['setting']['ff'])
