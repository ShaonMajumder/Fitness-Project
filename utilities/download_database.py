from mysql_database import *
from utility import *

utilization_directory = '../safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)


google_sheet_client_id = config['GOOGLE_SHEET']['google_sheet_client_id']
google_sheet_client_secret = config['GOOGLE_SHEET']['google_sheet_client_secret']

google_sheet_id = config['GOOGLE_SHEET']['spreadsheet_id']
google_sheet_range = config['GOOGLE_SHEET']['spreadsheet_range']
mydb.import_table_from_google_sheet(utilization_directory+'credentials.json',google_sheet_id,google_sheet_range,'nutrition_values')
#mydb.remove_temp()
print("Done...")