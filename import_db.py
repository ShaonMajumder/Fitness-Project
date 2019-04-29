import pandas as pd
import configparser
import codecs
from utilities.mysql_database import *
config = configparser.ConfigParser()
config.readfp(codecs.open("config.ini", "r", "utf8"))

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)
mydb.help()