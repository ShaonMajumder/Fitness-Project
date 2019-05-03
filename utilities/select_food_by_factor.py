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

def adjust_structure_nutrition_value():
	create_food_id()
	grams_columns = ['Amount_grams', 'Calories', 'Total_Carbohydrate_grams', 'Dietary_Fiber_grams', 'Sugar_grams', 'Protien_grams', 'Total_Fat_grams', 'Saturated_Fat_grams', 'Polyunsaturated_Fat_grams', 'Monounsaturated_Fat_grams', 'Trans_Fat_grams', 'Cholesterol_grams']
	for column in grams_columns:
		query = f"""ALTER TABLE `nutrition_values` CHANGE `{column}` `{column}` float"""
		mydb.execute(query)

	query = f"""ALTER TABLE `nutrition_values` CHANGE `id` `id` int"""
	mydb.execute(query)

def sort_by_nutrition(target_nutrition,ORDER='DESC'):
	#sort by target nutrition
	#Avaialble Factors ['Calories', 'Total_Carbohydrate_grams', 'Dietary_Fiber_grams', 'Sugar_grams', 'Protien_grams', 'Total_Fat_grams', 'Saturated_Fat_grams', 'Polyunsaturated_Fat_grams', 'Monounsaturated_Fat_grams', 'Trans_Fat_grams', 'Cholesterol_grams']
	query = f"""SELECT * FROM `nutrition_values` ORDER BY {target_nutrition} {ORDER}"""
	results = mydb.execute(query)
	for row in results:
		print(row['Name'])

def sort_by_biological_value():
	#digestion_Factor
	pass
def sort_by_price(price = ['cheap','costly']):
	if cheap == 'cheap':
		query = 'ASC'
def sort_by_inventory_availability():
	pass


#adjust_structure_nutrition_value()
#sort_by_nutrition('Total_Carbohydrate_grams')
sort_by_nutrition('Protien_grams')
sort_by_inventory_availability()
# Food Choose For Daily Diet Plan
# Combine heavy nutrition and more availability to pick a food
# Then Consider Price at last to sort to pick a food or you can escape

# Buy list for inventory
# Combine heavy nutrition and more availability in market pick a food
# Then Consider Price at last to sort to pick a food

# Then Consider health factors on heavy nutrition, which can rise other nutrients excessively

sort_by_price(price = ['cheap','costly'])

#combine 3 factor in food pick
#Egg Full = 34*.16 + 66*.11 = 12.7
#Wheigh the average raw egg shell, minus that from total weigh of a raw egg
#Whenever you weigh a egg, always minus the egg shell weight