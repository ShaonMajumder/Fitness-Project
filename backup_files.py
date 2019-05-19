from utilities.mysql_database import *
from utilities.utility import *
from utilities.gsheet import *
import pandas as pd

utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
cred_json_file = utilization_directory+'sheet_credentials.json'

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

SPREADSHEET_ID = config['GOOGLE_SHEET']['spreadsheet_id']
google_sheet_range = config['GOOGLE_SHEET']['spreadsheet_range']
gsheet = Gsheet(cred_json_file,SPREADSHEET_ID)

def backup_nutrition_excel():
	values = gsheet.get_values(google_sheet_range)
	if not values:
	    print('No data found.')

	header = values.pop(0)
	df = pd.DataFrame(values, columns=header)
	df.set_index('id')
	df.to_excel(utilization_directory+"nutrition.xlsx", index=False)

def backup_mysql_database():
	#export the whole database to a sql file
	#save it to safe_directory
	pass

def backup_safe_directory():
	#upload the safe directory to google drive via api
	pass

backup_nutrition_excel()
backup_mysql_database()
backup_safe_directory()