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

db = pd.read_excel('nutrition_values.xlsx', encoding='utf-8')
#db.set_index('Id', inplace=True)
rows = db.shape[0]
a = 0
columns = list(db.columns)
rows = db['Id']

for row in rows:
	row_li = []
	for column in columns:
		row_li.append(db.loc[row,column])

data2d = []
for row in db.iterrows():
    index, data = row
    data2d.append(data.tolist())

for row_li in data2d:
	mydb.insert(columns,row_li,'nutrition_values')
