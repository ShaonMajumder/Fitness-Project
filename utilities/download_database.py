from mysql_database import *
from utility import *
from gsheet import *

utilization_directory = '../safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
cred_json_file = utilization_directory+'sheet_credentials.json'

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)


google_sheet_client_id = config['GOOGLE_SHEET']['google_sheet_client_id']
google_sheet_client_secret = config['GOOGLE_SHEET']['google_sheet_client_secret']

SPREADSHEET_ID = config['GOOGLE_SHEET']['spreadsheet_id']
google_sheet_range = config['GOOGLE_SHEET']['spreadsheet_range']
gsheet = Gsheet(cred_json_file,SPREADSHEET_ID)

mydb.import_table_from_google_sheet(utilization_directory+'credentials.json',SPREADSHEET_ID,google_sheet_range,'nutrition_values')
#mydb.remove_temp()

def create_food_id():
	results = mydb.select("*","`Food_Id` = ''","nutrition_values")
	for row in results:
		id_ = row['id']
		while(True):
			random_key = randomString(stringLength=8)
			result = mydb.select("*",f"""`Food_Id` = '{random_key}'""","nutrition_values")
			if result != ():
				pass
			else:
				break
		mydb.edit(['Food_Id'],[random_key],f"""`id`={id_}""","nutrition_values")

def update_food_id_at_google_sheet():
	results = mydb.select(['Food_Id'],"","nutrition_values")
	sheet_name = 'Sheet1'
	range_letter = range_letter = gsheet.get_rangename_from_column_name(SPREADSHEET_ID,'Sheet1','Food_Id')
	range_num = 1	
	for row in results:
		range_num = range_num + 1
		foodid = row['Food_Id']
		update_cell_range = sheet_name+"!"+range_letter+str(range_num)
		update_area_range = update_cell_range #AG44'
		gsheet.update_cell(update_area_range,update_cell_range,foodid)

def adjust_structure_nutrition_value():
	create_food_id()
	grams_columns = ['Amount_grams', 'Calories', 'Total_Carbohydrate_grams', 'Dietary_Fiber_grams', 'Sugar_grams', 'Protien_grams', 'Total_Fat_grams', 'Saturated_Fat_grams', 'Polyunsaturated_Fat_grams', 'Monounsaturated_Fat_grams', 'Trans_Fat_grams', 'Cholesterol_grams']
	for column in grams_columns:
		query = f"""ALTER TABLE `nutrition_values` CHANGE `{column}` `{column}` float"""
		mydb.execute(query)

	query = f"""ALTER TABLE `nutrition_values` CHANGE `id` `id` int"""
	mydb.execute(query)

adjust_structure_nutrition_value()
update_food_id_at_google_sheet()

print("Done...")
		
