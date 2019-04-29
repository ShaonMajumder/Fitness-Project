from utilities.mysql_database import *
from utilities.utility import *
import configparser
import codecs

week_days = ['monday', 'tuesday', 'wednesday', 'thursday',  'friday', 'saturday', 'sunday']
import datetime
week_day = datetime.datetime.today().weekday()
day = week_days[week_day]

config = configparser.ConfigParser()
config.readfp(codecs.open("safe_directory/config.ini", "r", "utf8"))

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

#8 digit activity_code of any activity of apps
fasting = True
activity_id = "324jkhs2"
#total printed page number made by apps , for counting cost
#count total cost of ink used by printer
print_number = str(1)
date = "29/04/2019"
day = day
time = "6:00AM"
person_name = "Shaon Majumder"
weight = "59kg"
blood_pressure = "80-120"
body_fat_percentage = "[Prev]15%"
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
	
	ex_string = str(count) + ". " + name + " - "+sets+"sets "+"x "+reps+"reps"
	if(weight): ex_string = ex_string + " x "+weight
	if(duration): ex_string = ex_string + " x "+duration
	#if(target_area): count total target muscles and their exercise hit number
	ex_strings = ex_strings + ex_string + "\n"

ex_strings = "Targets:Abs,Triceps,Legs\nTotal Intensitiy: 2000rem\n" + ex_strings
#Target_Intensity = "Total intensity of all exercises/Target_muscle_intensity"

stri = f"""*** Print after Night Sleep, Right with blue pen
activity_id: {activity_id}
print_number: {print_number}
Date: {date}
Day: {day}
Time: {time}
Name: {person_name}
----
Todays Profile-
Weight: {weight}
Blood Pressure: {blood_pressure}
Body Fat Percentage: {body_fat_percentage}
Sleep Hours: {sleep_hours}
Recovery Sleep Permitted: {recovery_sleep_permitted}
----
Preworkout:
Gym Time Max: 2hours30minutes
{ex_strings}
Postworkout:
----
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
##save the text file after print




write_file('TestFile.txt', stri,mode="w")

import os
os.startfile("TestFile.txt", "print")