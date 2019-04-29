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

#Name, sets, reps, weight
exercises = [['Roman Situps','3','10',''],\
['Twisting Situps','3','10',''],\
['Lying Situps','3','10','5kg'],\
['Cable Stress Overhead Extension','3','10','3bar'],\
['skipping','1','1000','']]


#if day == "" , import from saved plan
#all exercise should be in lower case
ex_strings = ""
for exercise in exercises:
	ex_name,ex_sets,ex_reps,ex_weight = exercise
	ex_string = ex_name + " - "+ex_sets+"sets "+"x "+ex_reps+"reps"
	if(ex_weight): ex_string = ex_string+" x "+ex_weight
	ex_strings = ex_strings + ex_string + "\n"


stri = """*** Print after Night Sleep
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
print(stri.format(**locals()))
##save the text file after print