#8 digit activity_code of any activity of apps
fasting = True
activity_id = "324jkhs2"
#total printed page number made by apps , for counting cost
#count total cost of ink used by printer
print_number = str(1)
date = "29/04/2019"
day = "Monday"
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

ex_days = ['cardio','legs','triceps','abs','lower back','biceps','shoulders','fore arms','chest','back']
#unique Id will help in case of name change
columns = ['workout_id', 'name', 'synonyms', 'sets', 'reps', 'weight', 'duration', 'bodypart_day']
exercises = [\
	['1sef2e','roman situps','','3','10','','','abs'],\
	['a22f2e','twisting roman situps','','3','10','','','abs'],\
	['1s3f2e','ground abs crunches','lying situps','3','10','5kg','','abs'],\
	['ase42e','lying leg raise','','3','10','','','abs'],\
	['asef5e','windsheild wiper','obliques leg twist', '3', '10', '', '','abs'],\
	['asef26','hollow body hold','','3','10','','25seconds','abs'],\
	['asef7e','plank walk pushup','','3','10','','','abs'],\
	['ase82e','wood chooper','obliques pull','3','10','','','abs'],\
	#['as9f2e','hyper extension','','1','10','','','lower back'],\
	['a0ef2e','paralel bar hanging push down','','3','6','','','triceps'],\
	['11ef2e','back angle bar pushup','','3','8','','','triceps'],\
	['as222e','close grip bar pushup','','3','10','','','triceps'],\
	['asef33','tricep overhead extension','','3','10','5kg,7.5kg,10kg','','triceps'],\
	['as442e','cable stress overhead extension','','3','10','3bar','','triceps'],\
	['55ef2e','skull crusher','','3','6','5kg','','triceps'],\
	['as662e','seated dumbell kickback','','3','10','5kg','','triceps'],\
	['asef77','leg extension','','3','10','4bar','','legs'],\
	['as882e','hack squat','','3','10','40kg,55kg,65kg','','legs'],\
	['99ef2e','leg press','','3','10','85kg,95kg,105kg','','legs'],\
	['as002e','hill press','metatarsal press','3','25','','','legs'],\
	['ase111','hyper extension','','2','10','','','lower back'],\
	['222f2e','skipping','','1','1000','','','cardio'],\

	['','','','','','','']
]


#if day == "" , import from saved plan
#all exercise should be in lower case
ex_strings = ""
for exercise in exercises:
	ex_id,ex_name,ex_synonyms,ex_sets,ex_reps,ex_weight,ex_duration,ex_part_day = exercise
	
	ex_string = ex_name + " - "+ex_sets+"sets "+"x "+ex_reps+"reps"
	if(ex_weight): ex_string = ex_string + " x "+ex_weight
	if(ex_duration): ex_string = ex_string + " x "+ex_duration
	#if(ex_target): count total target muscles and their exercise hit number
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