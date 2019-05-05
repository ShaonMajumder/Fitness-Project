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
	food_ids = []
	for row in results:
		food_ids.append(row['Food_Id'])
	return food_ids

def sort_by_biological_value():
	#digestion_Factor
	pass
def sort_by_price(ids,price = 'cheap'):
	if price == 'cheap':
		order = 'ASC'
	elif price == 'costly':
		order = 'DESC'
	ids = ids[:5]
	id_bracket_string = "('" + "','".join(ids) + "')"
	
	condition = f"""`Food_Id` IN {id_bracket_string} ORDER BY `Recent_Market_Price` {order}"""
	results = mydb.select("*",condition,'nutrition_values')
	print("Sorted by Price")
	for row in results:
		print(row['Name'])
		
def sort_by_inventory_availability():
	pass


#adjust_structure_nutrition_value()
#sort_by_nutrition('Total_Carbohydrate_grams')
protein_food_ids = sort_by_nutrition('Protien_grams')
sort_by_price(protein_food_ids, price = 'cheap')
## Combine heavy nutrition and more availability to pick a food
# Then Consider Price at last to sort to pick a food or you can escapesort_by_inventory_availability()
#Finish the inventory
#sort by inventory_availability

# Food Choose For Daily Diet Plan
# Combine heavy nutrition and more availability to pick a food
# Then Consider Price at last to sort to pick a food or you can escape

# Buy list for inventory
# Combine heavy nutrition and more availability in market pick a food
# Then Consider Price at last to sort to pick a food

# Then Consider health factors on heavy nutrition, which can rise other nutrients excessively




#combine 3 factor in food pick
#Egg Full = 34*.16 + 66*.11 = 12.7
#Wheigh the average raw egg shell, minus that from total weigh of a raw egg
#Whenever you weigh a egg, always minus the egg shell weight



results = mydb.select('*',"",'nutrition_values')
purchasing_units = unique_items([row['Purchasing_Unit'] for row in results])
print(purchasing_units)



"""
Flow list
---------
[]
1. drink 5 litre water and eat at least after every 2 hour
1. complete inventory
name,purchase_digit,purchase_unit,
ginger,kg,.1,
garlic,kg,.1,
onion,kg,2,
green chilly,kg,.1,
coriander leaf,kg,.1,
tomato,kg,1
full egg,piece,6
banana,piece,8
peanut,kg,.5
chickpeas,kg,.5
chicken,kg,1.5
cucumber,
carrot,

2. Then calculate from their your meal plan.
3. Then calculate a way with micronutrients also.
4. food nutrition value wikipedia parser
"""