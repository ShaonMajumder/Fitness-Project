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

#8 digit activity_code of any activity of apps
fasting = True
activity_id = "324jkhs2"
#total printed page number made by apps , for counting cost
#count total cost of ink used by printer
print_number = str(1)
date = "29/04/2019"
day = "saturday"
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
print(columns)
#if day == "" , import from saved plan
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

def This_Week_Exercise_Form():
	This_Week_Exercise_Form = tkinter.Toplevel(Exercise_Section_Frame)
	This_Week_Exercise_Form.geometry("600x400")
	This_Week_Exercise_Form.title("Plan Meal")

	ex_results = mydb.select(['name'],"","workout_moves_data")
	ex_list_ = [result['name'] for result in ex_results]
	week_opvar = tkinter.StringVar()
	week_days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',  'friday']
	week_opvar.set(week_days[0])

	Day_Exercises_Planning_Day_Label =  tkinter.Label(This_Week_Exercise_Form, text = "Day")
	Day_Exercises_Planning_Day_Option = tkinter.OptionMenu(This_Week_Exercise_Form, week_opvar, *week_days) # command = select_category_action
	Day_Exercises_Planning_Exercises_Label = tkinter.Label(This_Week_Exercise_Form, text = "Exercise")
	Day_Exercises_Planning_Exercises_Entry = AutocompleteEntry(ex_list_, This_Week_Exercise_Form, bd = 2, width=30)
	Day_Exercises_Planning_Submit_Button = tkinter.Button(This_Week_Exercise_Form, text="Submit", command=add_exercises_to_weekly_plan)

	Day_Exercises_Planning_Day_Label.grid(sticky="w",row=1,column=1)
	Day_Exercises_Planning_Day_Option.grid(sticky="w",row=1,column=2)
	Day_Exercises_Planning_Exercises_Label.grid(sticky="w",row=1,column=3)
	Day_Exercises_Planning_Exercises_Entry.grid(sticky="w",row=1,column=4)
	Day_Exercises_Planning_Submit_Button.grid(sticky="w",row=2,column=1)




def add_exercises_to_weekly_plan():
	import datetime
	Day_Exercises = week_opvar.get()
	todays_day = datetime.datetime.now()
	
	results = mydb.select(['day_exercises'],"`day`='"+todays_day+"'","day_exercise_planning")
	if results == ():
		pass
	else:
		result = results[0]
		day_exercises = result['day_exercises']
		day_exercises_li = day_exercises.split(',')
		if Day_Exercises in day_exercises_li:
			pass
		else:
			day_exercises = day_exercises + "," + Day_Exercises
			mydb.edit(['day_exercises'],[day_exercises],"`day` = '"+todays_day+"'","day_exercise_planning")