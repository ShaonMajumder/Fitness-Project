from utilities.mysql_database import *
from utilities.utility import *
import configparser
import codecs

config = configparser.ConfigParser()
config.readfp(codecs.open("safe_directory/config.ini", "r", "utf8"))

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

def get_today_day():
	import datetime
	week_days = ['monday', 'tuesday', 'wednesday', 'thursday',  'friday', 'saturday', 'sunday']
	week_day = datetime.datetime.today().weekday()
	day = week_days[week_day]
	return day


#8 digit activity_code of any activity of apps
fasting = True
activity_id = "324jkhs2"
#total printed page number made by apps , for counting cost
#count total cost of ink used by printer
print_number = str(1)
date = "29/04/2019"
day = get_today_day()
time = "6:00AM"
person_name = "Shaon Majumder"
todays_body_weight = "59kg"
last_weight_calculate_datetime = '2-5-19 8:00 AM'
blood_pressure = "80-120"
last_blood_pressure_calculate_datetime = '2-5-19 8:00 AM'
body_fat_percentage = "15%"
body_fat_percentage_calculate_datetime = 'Today 8:00 AM'
sleep_hours = "7hours23minutes"
recovery_sleep_permitted = "30minutes"
if(fasting): fasting_time = "12:00AM-6:00PM"
else: fasting_time = "No" # try not print if fasting is not needed
bath = "Soap/Water Only/Shampoo/Soap and Shampoo"

ex_days = ['cardio','legs','triceps','abs','lower back','biceps','shoulders','fore arms','chest','glutes','back']
#unique Id will help in case of name change

columns = mydb.get_columns('workout_moves_data')

#all exercise should be in lower case
ex_strings = ""
count = 0
results = mydb.select('*',"","workout_moves_data")



#results = mydb.select('*',"`day`='"+day+"'","workout_moves_data")
results = mydb.select(['day_exercises_ids'],"`day`='"+day+"'","day_exercise_planning")
result = results[0]
exercise_ids = result['day_exercises_ids']
exercise_ids_li = exercise_ids.split(',')

results_ = []
for exercise_id in exercise_ids_li:
	results = mydb.select('*',"`workout_id`='"+exercise_id+"'","workout_moves_data")
	result = results[0]
	results_.append(result)


part_count_dic = {}
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


stri = f"""*** Print after Night Sleep, Right with blue pen
activity_id: {activity_id}
print_number: {print_number}
Date: {date}
Day: {day}
Time: {time}
Name: {person_name}
------------------------ Todays Physiological Parameters ------------------------
Sleep Hours: {sleep_hours}
You can sleep more: {recovery_sleep_permitted}
Target Consumption Calorie: 

Weight: {todays_body_weight} ({last_weight_calculate_datetime})
Blood Pressure: {blood_pressure} ({last_blood_pressure_calculate_datetime})
Body Fat Percentage: {body_fat_percentage} ({body_fat_percentage_calculate_datetime})
------------------------ Gym ------------------------
Note: Do warmupset of every exercise with light weight or do seperate warmup for 1 group of muscles.

Gym Time Max: 2hours30minutes
Targets:{target_parts}

Preworkout: Chola, Banana, Egg - 1 hour before workout
{ex_strings}
Postworkout: Water, Banana After workout

Summary {part_count_dic}
Total Intensitiy:{Target_Intensity}
------------------------ Inventory ------------------------
Inventory Empty: Banana, Chicken
----
You have loaded too much carb.
So today only 50grams of carb, and other ratio the same.
Fasting: {fasting_time}
Meal1:
Meal2:
Meal3:
.....
Bath: {bath}
Nail_Cut: Yes
Hair_Cut: Yes,Army Cut
Tooth_Brush: 
Hygene Instructions:
"""
#print(stri.format(**locals()))
print(stri)
"""
3 body part can reduce rest time
Daily abs training can help abs and cut the vacum slot at sunday


In home exercise:
6. hollow body hold - 3sets x 10reps x 25seconds
7. plank walk pushup - 3sets x 10reps
"""
"""
strings = []
for c in range(39):
	while(True):
		rands = randomString(stringLength=8)
		if rands in strings:
			pass
		else:
			break
	strings.append(rands)


for c in strings:
	print(c)

write_file('TestFile.txt', stri,mode="w")

##save the text file after print
import os
import win32print

printer_name = "Canon LBP6030/6040/6018L"
win32print.SetDefaultPrinter(printer_name)

os.startfile("TestFile.txt", "print")

"""