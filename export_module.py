from utilities.mysql_database import *
from utilities.utility import *
from utilities.science import *
from utilities.select_food_by_factor import *
import datetime



dbconfig = read_config_ini("safe_directory/dbconfig.ini")
host=dbconfig['DATABASE']['host']
user=dbconfig['DATABASE']['user']
password=dbconfig['DATABASE']['password']
db=dbconfig['DATABASE']['db']
charset=dbconfig['DATABASE']['charset']
cursorclass=dbconfig['DATABASE']['cursorclass']
mydb = mysql_db(host, user, password, db, charset, cursorclass)

def export_module(profile_id,export_as,debug):
	# Export as File - file
	# Export as Print - print

	while(True):
		rands_ = randomString(stringLength=8)
		result = mydb.select('*','`activity_id` = \''+rands_+'\'','activities')
		if result == ():
			break


	#8 digit activity_code of any activity of apps
	activity_id = rands_
	
	## calculate print number
	result = mydb.select('*','`activity_type`=\'print\' and `profile_id`=\''+profile_id+'\'','activities')
	#total printed page number made by apps , for counting cost
	#count total cost of ink used by printer
	print_number = str(len(result))

	today = datetime.date.today()
	date = today.strftime('%d %b,%Y')
	day = get_today_day()#"saturday"
	time = "6:00AM"
	
	results = mydb.execute(f"""SELECT * FROM biodata INNER JOIN profiles ON biodata.profile_id = profiles.profile_id WHERE profiles.`profile_id` = '{profile_id}'""")
	row = results[0]

	fullname = row['fullname']
	gender = row['gender']
	age = row['age']
	birthdate = row['birthdate']
	protein_grams_per_body_pound = row['protein_grams_per_body_pound']
	height = row['height']
	bodyweight = row['bodyweight']
	meal_number = row['meal_number']
	activity_level = row['activity_level']

	DOCUMENT_ID_STRING = f"""activity_id: {activity_id}  | print_number: {print_number}
	Name: {fullname}  | Date: {date}  | Day: {day}  | Time: {time}"""

	todays_body_weight = bodyweight
	last_weight_calculate_datetime = '2-5-19 8:00 AM'
	blood_pressure = "80-120"
	last_blood_pressure_calculate_datetime = '2-5-19 8:00 AM'
	body_fat_percentage = "15%"
	body_fat_percentage_calculate_datetime = 'Today 8:00 AM'
	sleep_hours = "7hours23minutes"
	recovery_sleep_permitted = "30minutes"
	bath = "Soap/Water Only/Shampoo/Soap and Shampoo"


	""" Gym Calculation """
	#unique Id will help in case of name change
	ex_days = ['cardio','legs','triceps','abs','lower back','biceps','shoulders','fore arms','chest','glutes','back']
	#all exercise should be in lower case
	#results = mydb.select('*',"`day`='"+day+"'","workout_moves_data")
	results = mydb.select(['day_exercises_ids'],"`day`='"+day+"'","day_exercise_planning")
	#print(results)

	result = results[0]
	exercise_ids = result['day_exercises_ids']
	exercise_ids_li = exercise_ids.split(',')

	results_ = []
	for exercise_id in exercise_ids_li:
		results = mydb.select('*',"`workout_id`='"+exercise_id+"'","workout_moves_data")
		result = results[0]
		results_.append(result)

	part_count_dic = {}
	count = 0
	ex_strings = ""
	for result in results_:
		count = count + 1
		
		id_=result['id']
		workout_id=result['workout_id']
		name=result['name']
		synonyms=result['synonyms']
		type_=result['type']
		instrument=result['instrument']
		sets=result['sets']
		reps=result['reps']
		weight=result['weight']
		duration=result['duration']
		bodypart_day=result['bodypart_day']
		target_area=result['target_area']
		demo=result['demo']
		comment=result['comment']
		
		if bodypart_day in part_count_dic:
			part_count_dic[bodypart_day] = part_count_dic[bodypart_day] + 1
		else:
			part_count_dic[bodypart_day] = 1
		
		ex_string = str(count) + ". " + name + " - "+sets+"sets "+"x "+reps+"reps"
		if(weight): ex_string = ex_string + " x "+weight
		if(duration): ex_string = ex_string + " x "+duration
		#if(target_area): count total target muscles and their exercise hit number
		ex_strings = ex_strings + ex_string + "\n"
	ex_strings = ex_strings[:-1]
	target_parts = [part for part in part_count_dic if part_count_dic[part] > 3]
	target_parts = ','.join(target_parts)

	#Count Total intensity
	#Target_Intensity = "Total intensity of all exercises/Target_muscle_intensity"
	Target_Intensity = "2000rem"

	GYM_STRING = f"""------------------------ Gym ------------------------
	Note: Do warmupset of every exercise with light weight or do seperate warmup for 1 group of muscles. Build mind muscle connection in every exercise.
	*** Take Postworkout Meal box,Gym IDCard,Bandage,Towel in Gym Bag

	Gym Time Max: 2hours30minutes
	Targets:{target_parts}

	Take Preworkout Meal Box before 1 hour
	{ex_strings}
	Take Postworkout Meal Box after workout

	Summary {part_count_dic}
	"""

	""" Nutrition Calculation """
	fasting = True
	if(fasting): fasting_time = "12:00AM-6:00PM"
	else: fasting_time = "No" # try not print if fasting is not needed
	calorie_intake,protein_requirement_g,carbohydrate_requirement_g,fat_requirement_g,per_meal_protein_requirement_g,per_meal_carbohydrate_requirement_g,per_meal_fat_requirement_g,food_list = generate_food_list()

	#pick by price and availability in inventory
	NUTRITION_STRING = f"""------------------------ Nutrition ------------------------
	Target CALORIE: {calorie_intake} Kcal | Meal Number: {mealnumber}
	Macros - {round(protein_requirement_g,2)}g Protein|{round(fat_requirement_g,2)}g Fat|{round(carbohydrate_requirement_g,2)}g Carb
	Per meal - {round(per_meal_protein_requirement_g,2)}g Protein|{round(per_meal_fat_requirement_g,2)}g Fat|{round(per_meal_carbohydrate_requirement_g,2)}g Carb

	Mix Bowl>> {food_list}
	"""

	PHYSIOLOGICAL_STRING = f"""------------------ Todays Physiological Parameters ------------------
	Sleep Hours: {sleep_hours}  | You can sleep more: {recovery_sleep_permitted}
	Weight: {todays_body_weight} ({last_weight_calculate_datetime}) | Body Fat Percentage: {body_fat_percentage} ({body_fat_percentage_calculate_datetime})
	Blood Pressure: {blood_pressure} ({last_blood_pressure_calculate_datetime}) | Goal: {fitness_goal}"""

	stri = f"""*** Print after Night Sleep, Right with blue pen
	{DOCUMENT_ID_STRING}
	{PHYSIOLOGICAL_STRING}
	{GYM_STRING}
	{NUTRITION_STRING}
	------------------------ Inventory ------------------------
	Inventory Empty: Banana, Chicken
	--------------- Todays Work ----------------
	Bath: {bath}
	Nail_Cut: Yes
	Hair_Cut: Yes,Army Cut
	Tooth_Brush: 
	Hygene Instructions:
	"""
	#print(stri.format(**locals()))
	stri = stri.replace('\n','\r\n')
	if(debug): print(stri)
	output_file = date+'.txt'
	if export_as == 'file':
		write_file(output_file, stri,mode="w")
		#delete output_file
	elif export_as == 'print':
		printer_file(output_file)
		#delete output_file


export_module('vwjjn6ip','file',True)
"""
Flow List
1. Intensity calculation Total Intensitiy:2000rem
"""
