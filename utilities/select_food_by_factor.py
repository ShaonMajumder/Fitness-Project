try:
	from utilities.mysql_database import *
except:
	from mysql_database import *
try:
	from utilities.utility import *
except:
	from utility import *
try:
	from utilities.science import *
except:
	from science import *

utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
goal_config =read_config_ini("Goal.data")

##database config
host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)
###database config

##meal goal config
gender = goal_config['PHYSIQUE']['gender']
age = goal_config['PHYSIQUE']['age']
height = goal_config['PHYSIQUE']['height']
bodyweight = goal_config['PHYSIQUE']['bodyweight']
activity_level = goal_config['ROUTINE']['activity_level']
protein_grams_per_body_pound = goal_config['CALORIE']['protein_grams_per_body_pound']
mealnumber = goal_config['ROUTINE']['mealnumber']
fitness_goal = goal_config['GOAL']['goal']
## params: gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal
###meal goal config


def sort_by_nutrition_old(target_nutrition,ORDER='DESC'):
	#sort by target nutrition
	#Avaialble Factors ['Calories', 'Total_Carbohydrate_grams', 'Dietary_Fiber_grams', 'Sugar_grams', 'Protein_grams', 'Total_fat_grams', 'Saturated_Fat_grams', 'Polyunsaturated_Fat_grams', 'Monounsaturated_Fat_grams', 'Trans_Fat_grams', 'Cholesterol_grams']
	query = f"""SELECT * FROM `nutrition_values` ORDER BY {target_nutrition} {ORDER}"""
	results = mydb.execute(query)
	food_ids = []
	for row in results:
		food_ids.append(row['Food_Id'])
	return food_ids

def sort_by_nutrition(food_ids,target_nutrition,ORDER='DESC'):
	#sort by target nutrition
	#Avaialble Factors ['Calories', 'Total_Carbohydrate_grams', 'Dietary_Fiber_grams', 'Sugar_grams', 'Protein_grams', 'Total_fat_grams', 'Saturated_Fat_grams', 'Polyunsaturated_Fat_grams', 'Monounsaturated_Fat_grams', 'Trans_Fat_grams', 'Cholesterol_grams']
	food_ids_str = "('" + "','".join(food_ids) + "')"
	query = f"""SELECT * FROM `nutrition_values` WHERE `Food_Id` IN {food_ids_str} ORDER BY {target_nutrition} {ORDER}"""
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


#create the meal plan
#findout the macro need
#loop through each macro
#	find the macro and sort the inventory according to their availability & quantity & price
#	if less food then create buy list according to price



#protein_food_ids = sort_by_nutrition('Protein_grams',ORDER='DESC')
#sort_by_price(protein_food_ids, price = 'cheap')

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
#Egg Fat = 34*.27 + 66*.002
#Egg Carb = 34*.036 + 66*0.007
#Wheigh the average raw egg shell, minus that from total weigh of a raw egg
#Whenever you weigh a egg, always minus the egg shell weight

#results = mydb.select('*',"",'nutrition_values')
#purchasing_units = unique_items([row['Purchasing_Unit'] for row in results])
#print(purchasing_units)




def calculate_protein_iso(results, target_macro,requirement_g,threshold_level):
	total_protein = 0
	total_carb = 0
	total_fat = 0
	
	for row in results:
		print(row['Total_fat_grams'])
		sync = 'Total_Carbohydrate_grams'
		synp = 'Protein_grams'
		synf = 'Total_fat_grams'
		if row[synp] > threshold_level[synp] or row[synp] == threshold_level[synp]:
			total_carb = total_carb + row[synp]
		if row[sync] > threshold_level[sync] or row[sync] == threshold_level[sync]:
			total_protein = total_protein + row[sync]
		if row[synf] > threshold_level[synf] or row[synf] == threshold_level[synf]:
			total_fat = total_fat + row[synf]

	_ = []
	for row in results:
		if row[target_macro] < threshold_level[target_macro]:
			continue
		else:
			print(target_macro+" "+row['Name'],row[target_macro])

		#target is maximizing the protein value, minimizing other marginal value
		row['relative_protein'] = float(row['Protein_grams'])/total_protein
		#print(total_fat)
		row['relative_fat_margin'] = 1 - float(row['Total_fat_grams'])/total_fat
		row['relative_carb_margin'] = 1 - float(row['Total_Carbohydrate_grams'])/total_carb
		
		row['total_score'] = row['relative_protein'] + row['relative_fat_margin'] + row['relative_carb_margin']
		row['relative_score'] = row['total_score']/3

		row['quantity_'+target_macro] =  row['relative_score']*requirement_g[target_macro]
		if 'quantity_' in row:
			row['quantity_'] = row['quantity_'] + (100/row[target_macro])*row['quantity_'+target_macro]
			print("Repeat",row['quantity_'])
		else:
			row['quantity_'] = (100/row[target_macro])*row['quantity_'+target_macro]
			if row['Name'] == 'egg full':
				print("Repeat",row['quantity_'])

		
		row['relative_score_'+target_macro] = row['relative_score']
		_.append(row)

	results = _
	return results

def calculate_portion(results, target_macro,requirement_g,threshold_level,sort=False,debug=False):
	if(debug): print("Calculation of "+target_macro)
	total_macro = 0
	total_weight = 0
	total_mass_per_credit = 0
	for row in results:
		if row[target_macro] > threshold_level or row[target_macro] == threshold_level:
			total_macro = total_macro + row[target_macro]
			total_mass_per_credit = total_mass_per_credit + float(row['Unit_grams'])/float(row['Recent_Market_Price'])
			total_weight = total_weight + row['weight']
	
	#targets=maximum_avail,lowest_quantity_more_nutri_dense,less_cost
	_ = []
	for row in results:
		row['relative_weight'] = float(row['weight'])/total_weight
		mass_per_credit = float(row['Unit_grams'])/float(row['Recent_Market_Price'])
		row['relative_mass_in_unit_price'] = mass_per_credit/total_mass_per_credit

		if row[target_macro] < threshold_level:
			if 'quantity_' in row:
				pass
				#row['quantity_'] = row['quantity_'] + 0
			else:
				row['quantity_'] = 0
		else:
			if(debug): print(target_macro+" "+row['Name'],row[target_macro])
			row['relative_macro'] = float(row[target_macro])/total_macro	
			row['total_score'] = row['relative_weight'] + row['relative_macro'] + row['relative_mass_in_unit_price']
			row['relative_score'] = row['total_score']/3


			row_alloted_quantity =  row['relative_score']*requirement_g
			if 'quantity_' in row:
				row['quantity_'] = row['quantity_'] + (100/row[target_macro])*row_alloted_quantity
				if(debug): print("Repeat",row['quantity_'])
			else:
				row['quantity_'] = (100/row[target_macro])*row_alloted_quantity

		_.append(row)

	results = _

	if(sort):
		def func(row):
			return row['relative_score']
		results = reversed(sorted(results, key = func))
		
	return results

def calculate_food_list(results,macro_li,requirement_g,threshold_level_dic,debug=False):
	P = F = C = 0
	results = calculate_portion(results, macro_li[0],requirement_g[macro_li[0]],threshold_level=threshold_level_dic[macro_li[0]])
	for row in results:
		F = F + (row['Total_fat_grams']/100) * row['quantity_']
		C = C + (row['Total_Carbohydrate_grams']/100) * row['quantity_']
		P = P + (row['Protein_grams']/100) * row['quantity_']
	if(debug): print(f"""Carb sec -Protein = {P}\nCarb = {C}\nFat = {F}""")

	if macro_li[1] == 'Protein_grams':
		K = P
	elif macro_li[1] == 'Total_Carbohydrate_grams':
		K = C
	elif macro_li[1] == 'Total_fat_grams':
		K = F
	requirement_g_ = requirement_g[macro_li[1]] - K
	if(requirement_g_ > 0):
		P = F = C = 0
		results = calculate_portion(results, macro_li[1], requirement_g_,threshold_level=threshold_level_dic[macro_li[1]])
		for row in results:
			C = C + (row['Total_Carbohydrate_grams']/100) * row['quantity_']
			F = F + (row['Total_fat_grams']/100) * row['quantity_']
			P = P + (row['Protein_grams']/100) * row['quantity_']
		if(debug): print(f"""Protein Sec - Protein = {P}\nCarb = {C}\nFat = {F}""")

	if macro_li[2] == 'Protein_grams':
		K = P
	elif macro_li[2] == 'Total_Carbohydrate_grams':
		K = C
	elif macro_li[2] == 'Total_fat_grams':
		K = F
	requirement_g_ = requirement_g[macro_li[2]] - K
	if(requirement_g_ > 0):
		P = F = C = 0
		results = calculate_portion(results, macro_li[2],requirement_g_,threshold_level=threshold_level_dic[macro_li[2]])
		for row in results:
			F = F + (row['Total_fat_grams']/100) * row['quantity_']
			C = C + (row['Total_Carbohydrate_grams']/100) * row['quantity_']
			P = P + (row['Protein_grams']/100) * row['quantity_']
		if(debug): print(f"""Fat Sec - Protein = {P}\nCarb = {C}\nFat = {F}""")

	return results,P,C,F

def printable_unit_conversion(results):
	_ = []
	for row in results:
		if row['unit'] == 'piece':
			piece = float(row['quantity_'])/float(row['Actual_unit_weight_grams'])
			piece_ = round(piece)
			#print(row['Name'],piece,round(piece_))
			row['print_digit'] = piece_
			row['print_unit'] = 'pieces'
		else:
			row['print_digit'] = row['quantity_']
			row['print_unit'] = 'grams'
		_.append(row)
	return _


def return_food_string(results):
	food_list = printable_unit_conversion(results)
	P=C=F=0
	string = []
	for row in food_list:
		string.append(f"""{row['Name']} {row['print_digit']:.2f} {row['print_unit']}""")
		F = F + (row['Total_fat_grams']/100)*row['quantity_']
		C = C + (row['Total_Carbohydrate_grams']/100)*row['quantity_']
		P = P + (row['Protein_grams']/100)*row['quantity_']
	return ','.join(string)

def check_macro_result(results):
	P=C=F=0
	for row in results:
		F = F + (row['Total_fat_grams']/100)*row['quantity_']
		C = C + (row['Total_Carbohydrate_grams']/100)*row['quantity_']
		P = P + (row['Protein_grams']/100)*row['quantity_']

	print("Double Check Total Macro from food\nP|C|F=",P,C,F)



def generate_food_list():
	#Algorithm Starts
	foods_in_inventory = mydb.select('*','','food_inventory')
	inventory_food_ids = [row['Food_Id'] for row in foods_in_inventory]
	query = f"""SELECT * FROM `nutrition_values` WHERE `Food_Id` IN {"('" + "','".join(inventory_food_ids) + "')"}"""
	results = mydb.execute(query)

	# getting the food_id and invetory weight
	_ = []
	for row in results:
		for row2 in foods_in_inventory:
			if row['Food_Id'] == row2['Food_Id']:
				row['weight'] = row2['weight']
				row['unit'] = row2['unit']
				break
		_.append(row)
	results = _

	##Calculate Macro Need
	result_macro = nutrition_calculator(gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal,debug=False)
	calorie_intake,protein_requirement_g,carbohydrate_requirement_g,fat_requirement_g,per_meal_protein_requirement_g,per_meal_carbohydrate_requirement_g,per_meal_fat_requirement_g = result_macro
	result_stri = f"""Result,
		Your Daily CALORIE intake: {calorie_intake} Kcal
		Your Daily Macros - {round(protein_requirement_g,2)}g Protein|{round(fat_requirement_g,2)}g Fat|{round(carbohydrate_requirement_g,2)}g Carbohydrate
		Your need to eat per meal - {round(per_meal_protein_requirement_g,2)}g Protein|{round(per_meal_fat_requirement_g,2)}g Fat|{round(per_meal_carbohydrate_requirement_g,2)}g Carbohydrate"""
	#print(result_stri)


	requirement_g = {
		'Protein_grams' : protein_requirement_g,
		'Total_Carbohydrate_grams' : carbohydrate_requirement_g,
		'Total_fat_grams' : fat_requirement_g
	}

	#arranging higher macro value to lower
	def func(row):
		return requirement_g[row]
	r = sorted(requirement_g, key = func)
	macro_li = r[::-1]

	threshold_level_dic = {
		'Total_Carbohydrate_grams': 17,
		'Protein_grams': 4,
		'Total_fat_grams': 7
	}

	results,P,C,F = calculate_food_list(results,macro_li,requirement_g,threshold_level_dic)
	resu = f"""Todays Deficit
	Protein = {protein_requirement_g - P}
	Carbohydrate = {carbohydrate_requirement_g - C}
	Fat = {fat_requirement_g - F}
	Note: Add this quantity to tomorrow's"""
	#print(resu)

	return calorie_intake,protein_requirement_g,carbohydrate_requirement_g,fat_requirement_g,per_meal_protein_requirement_g,per_meal_carbohydrate_requirement_g,per_meal_fat_requirement_g,return_food_string(results)

#selection of carb is bad , choose from less fat, less protein source like rice and later fuse together with new idea like dietary fiber
#Find the protein foods
#	then sort them according to macro
#	then check if enough macro is there

"""
Flow list
---------
3. Then calculate a way with micronutrients also.
4. Save purchase history of food with date and price
5. How to divide meal box, post and preworkout meal box
Meal Box 1: Egg Full-1,Chicken(1p)-30g,<Mix-Bowl>/4,Water-1Litre
Meal Box 2: Egg Full-1,Chicken(1p)-30g,<Mix-Bowl>/4,Water-1Litre
Meal Box 3: Egg Full-1,<Mix-Bowl>/4,Water-1Litre
Meal Box 4: Egg Full-1,Fish(1p)-30g,<Mix-Bowl>/4,Water-1Litre
Preworkout Meal Box: Chola(1.5palm)-30g, Banana(2pieace)-100g
Postworkout Meal Box: Take Adjacent Meal according to hour
6. Fasting Calculator
	Fasting: 12:00AM-6:00PM
7. Caution for deficit or surplus from previous or overall goal calorie till a date
	Caution: Previously, You have loaded too much carb;so only 50grams of carb allowed and other ratio the same.

Must Dos: drink 5 litre water and eat at least after every 2 hour
"""