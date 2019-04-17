### Calorie Calculator - https://www.freedieting.com/calorie-calculator
### Katch-McArdle Formula: Enter Body Fat % 
### Body Fat Calculator - https://www.freedieting.com/body-fat-calculator
### Find food requirement based on Body fat percentage, learn how to measure body fat percentage
### Muscle Tape - https://www.daraz.com.bd/products/te-1-pc-simple-cnvenient-body-tape-measure-for-measuring-waist-diet-weight-loss-i103024775-s1017430360.html?spm=a2a0e.searchlist.list.7.77282e39nkmCcz&search=1
### Fat Caliper - https://www.daraz.com.bd/catalog/?q=fat+caliper
### bmr activity multiplier for weight lifters
### Body fat% for 6 pack calculation - https://www.youtube.com/watch?v=j4zOuCYYCcs

import argparse
import configparser
import codecs
import tkinter

unit_kg_to_pounds = 2.20462
unit_feet_to_centimeters = 30.48
unit_feet_to_inches = 12
unit_inch_to_centimeters = 2.54

def One_Rep_Max(Regular_Rep,Regular_Weight):
	return Regular_Weight/0.75

def One_Rep_Max(Regular_Rep,Regular_Weight):
	Volume = Regular_Rep * Regular_Weight 
	Rep_Max = Regular_Weight + (Volume * .033)
	return Rep_Max

def feet_to_cm(feet):
	return unit_feet_to_centimeters*feet

def inch_to_cm(inch):
	return unit_inch_to_centimeters*inch

def estimate_body_fat(height_in_cm,weight_in_kg,gender):
	"""
	Based on - https://www.youtube.com/watch?v=6QKPMtib6Ko
	result 2-3% tolerance
	"""
	if gender == 'male':
		ideal_body_weight = height_in_cm - 100
		over_or_under_weight = weight_in_kg - ideal_body_weight
		if over_or_under_weight > 0:
			over_or_under_weight_flag = 'over_weight'
		else:
			over_or_under_weight_flag = 'under_weight'
			if int(over_or_under_weight) > 10:
				ValueError("More than 10 kilo under weight extremely ectomorph - skinny, long with more fat. So we can not estimate your body weight.")
		#For male, Ideal fat% = 15%
		fat_percentage = 15+int(over_or_under_weight)

	elif gender == 'female':
		ideal_body_weight = height_in_cm - 105
		over_or_under_weight = weight_in_kg - ideal_body_weight
		if over_or_under_weight > 0:
			over_or_under_weight_flag = 'over_weight'
		else:
			over_or_under_weight_flag = 'under_weight'
			if int(over_or_under_weight) > 10:
				ValueError("More than 10 kilo under weight extremely ectomorph - skinny, long with more fat. So we can not estimate your body weight.")
		#For female, Ideal fat% = 20%
		fat_percentage = 20+int(over_or_under_weight)

	return fat_percentage
	
	





def bmr(gender,weight_in_kg,height_in_cm,age_in_years):
	if gender == 'male':
		BMR = (10 * weight_in_kg) + (6.25 * height_in_cm) - (5 * age_in_years) + 5
	elif gender == 'female':
		BMR = (10 * weight_in_kg) + (6.25 * height_in_cm) - (5 * age_in_years) - 161

	return BMR
	
def Maintenance_Calories_Per_Day(BMR,activity_level):
	"""
	Estimating Calories for Weight Loss
	After calculating the BMR, exercise is factored in. Depending on the exercise level chosen, the BMR will be multiplied by anything from 1.2 to 1.9.

	This provides us with maintenance calories – the amount of calories you could consume each day and neither lose or gain weight.

	To get the fat loss figure – 20% of calories is subtracted.

	The extreme fat loss figure has 40% subtracted. However – there is a “rock bottom” figure that equates to 8 calories per pound of body weight – the extreme fat loss will never be less than this amount. This has been put into the calculator as a failsafe to prevent users from embarking on highly-restricted diets. Such diets need medical care, advice, and monitoring.

	It is also not advised to drastically reduce calories, but rather do so gradually or by a maximum of 500 calories per day.
	"""
	"""
	1,1.2,1.375,1.55,1.725,1.9
	First method:: Following now
	Basal Metabolic Rate , Calorie_Per_day = BMR * 1
	Little/No exercise , Calorie_Per_day = BMR * 1.2
	3 times/week , Calorie_Per_day = BMR * 1.3 ~ 1.4 ~ 1.375
	4 times/week , Calorie_Per_day = BMR * 1.4 ~ 1.42
	5 times/week , Calorie_Per_day = BMR * 1.5 ~ 1.46
	Daily , Calorie_Per_day = BMR * 1.6 ~ 1.55
	5 times/week(Intense) , Calorie_Per_day = BMR * 1.7 ~ 1.64
	Daily(Intense) or Twice Daily , Calorie_Per_day = BMR * 1.8 ~ 1.73
	Daily exercise + Physical Job , Calorie_Per_day = BMR * 1.9
	
	activity_level_string = "Choices-\n0) Basal Metabolic Rate\n1)Little/No exercise\n2) 3 times/week\n3) 4 times/week\n4) 5 times/week\n5) Daily\n6) 5 times/week(Intense)\n7) Daily(Intense) or Twice Daily\n8) Daily exercise + Physical Job\nEnter 0-8 according to your choice. <::"
	activity_levels_multiplier = [1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9]
	or [1,1.2,1.4,1.42,1.46,1.55,1.64,1.73,1.9]
	"""
	"""
	Second method
	If you have no movement, you need to live, Calories_Per_Day = BMR * 1
	If you are sedentary (little or no exercise), Calories_Per_Day = BMR * 1.2
	If you are lightly active (light exercise or sports 1-3 days/week), Calories_Per_Day = BMR * 1.375
	If you are moderately active (moderate exercise 3-5 days/week), Calories_Per_Day = BMR * 1.55
	If you are very active (hard exercise 6-7 days/week), Calories_Per_Day = BMR * 1.725
	If you are super active (very hard exercise and a physical job), Calories_Per_Day = BMR * 1.9
	
	activity_level_string = "Choices -\n0) If you have no movement, you need to live\n1) If you are sedentary (little or no exercise)\n2) If you are lightly active (light exercise or sports 1-3 days/week)\n3) If you are moderately active (moderate exercise 3-5 days/week)\n4) If you are very active (hard exercise 6-7 days/week)\n5) If you are super active (very hard exercise and a physical job)\nEnter 0-5 according to your choice. <::"	
	activity_levels_multiplier = [1,1.2,1.375,1.55,1.725,1.9]
	"""
	activity_levels_multiplier = [1,1.2,1.375,1.419,1.463,1.55,1.638,1.725,1.9]
	#check if activity_level is int
	Calories_Per_Day = BMR * activity_levels_multiplier[activity_level]
	return round(Calories_Per_Day,0)


def kgs_to_lbs(kgs):
	return kgs*unit_kg_to_pounds

def lbs_to_kgs(lbs):
	return lbs/unit_kg_to_pounds

def filter_height_feet_inch(stri):
	stri = stri.replace(" ","")
	keyword_len = len('ft')

	for x in range(0,len(stri)-1):
		if stri[x:x+keyword_len] == 'ft':
			split2 = [stri[:x+keyword_len], stri[x+keyword_len:]]
			break
		elif stri[x:x+keyword_len] == 'in':
			split2 = [stri[:x+keyword_len], stri[x+keyword_len:]]
			break

	if 'ft' in split2[0]:
		feet_stri = split2[0]
		inch_stri = split2[1]
	elif 'ft' in split2[1]:
		feet_stri = split2[1]
		inch_stri = split2[0]
	else:
		raise ValueError("Feet unit is not present")

	feet_digit = feet_stri.split('ft')
	if not feet_digit[1] == '':
		raise ValueError("Invalid Character after feet unit (ft).")
	feet_digit= feet_digit[0]
	try:
		feet_digit = float(feet_digit)
	except ValueError:
		raise ValueError(feet_digit+"Feet digit is invalid.")

	if 'in' in inch_stri:
		inch_digit = inch_stri.split('in')
		if not inch_digit[1] == '':
			raise ValueError("Invalid Character after inch unit (in).")
		inch_digit= inch_digit[0]
	else:
		raise ValueError("Inch unit is not present")	
	try:
		inch_digit = float(inch_digit)
	except ValueError:
		raise ValueError(inch_digit+"Inch digit is invalid.")

	return feet_digit,inch_digit

def filter_age(stri):
	age = stri.replace(" ","")
	age_unit = "".join([c for c in age if c in ['y','r','s']])

	if age_unit == 'yrs':
		age_digit = stri.replace(age_unit,'')
		try:
			age_digit = float(age_digit)
			return age_digit, age_unit
		except ValueError:
			raise ValueError(age_digit+" is not a number")
			#return false
	else:
		raise ValueError(age_unit+" is invalid years unit. yrs can be accepted")
		#return false

def filter_mealnumber(stri):
	mealnumber = stri.replace(" ","")
	try:
		mealnumber = int(mealnumber)
		return mealnumber
	except ValueError:
		raise ValueError("Mealnumber "+mealnumber+" is invalid. Needs to be integer.")

def filter_calorie(stri):
	calorie = stri.replace(" ","")
	calorie_unit = "".join([c for c in calorie if c in ['k','c','a','l']])


	if calorie_unit == 'kcal':
		calorie_digit = stri.replace(calorie_unit,'')
		try:
			calorie_digit = float(calorie_digit)
			return calorie_digit, calorie_unit
		except ValueError:
			raise ValueError(calorie_digit+" is not a number")
			#return false
	else:
		raise ValueError(calorie_unit+" is invalid energy unit. kcal can be accepted")
		#return false

def filter_bodyweight(stri):
	body_weight = stri.replace(" ","")
	body_weight_unit = "".join([c for c in body_weight if c in ['k','g','l','b','s']])
	
	if body_weight_unit == 'kgs' or body_weight_unit == 'lbs':
		body_weight_digit = stri.replace(body_weight_unit,'')
		try:
			body_weight_digit = float(body_weight_digit)
			return body_weight_digit, body_weight_unit
		except ValueError:
			raise ValueError(body_weight_digit+" is not a number")
			#return false
	else:
		raise ValueError(body_weight_unit+" is invalid weight unit")
		#return false

## Defaults
protein_per_body_weight_g = 1.0
config = configparser.ConfigParser()
config.readfp(codecs.open("Goal.data", "r", "utf8"))

parser = argparse.ArgumentParser()
parser.add_argument("--inputsource", choices=['file', 'cli'], help="file - For take input saved from file.\ncli - for take inputs from argument or prompt. If not specified it takes from file.",type=str)
parser.add_argument("--bodyweight", help="Your bodyweight in kgs/lbs. Example: 60kgs or 60lbs",type=str)
parser.add_argument("--age", help="Your age in years. Example: 20yrs",type=str)
parser.add_argument("--gender", choices=['male', 'female'], help="Your gender. Example: male/female",type=str)
parser.add_argument("--height", help="Your height in feet-inch. Example: 5ft7in",type=str)
parser.add_argument("--goal", choices=['maintain','Lean_Bulking', 'gain', 'loose'], help="'Lean Bulking' for gaining muscle and cutting body fat at the same time. maintain' for maintaining your current body mass/'loose' for loosing body fat/'gain' for gaining muscle")
parser.add_argument("--mealnumber",help="Number of meals you can take a day. Ex: 4-8 is a good number with proper quantity of food.",type=str)
#parser.add_argument("--calorie_intake",help="Daily CALORIE amount in Kcal.",type=str)
parser.add_argument("--change_protein_per_body_pound",help="change_protein_per_body_pound.",type=str)

args = parser.parse_args()

run_mode = input("gui/cli <<:")
if run_mode == 'cli':
	pass
elif run_mode == 'gui':
	import tkinter

	def take_new_url():
		resource_url = E1.get()

	top = tkinter.Tk()
	top.title("Fitness-Project")
	top.geometry("500x500")

	L1 = tkinter.Label(top, text = "Resource Url")
	E1 = tkinter.Entry(top, bd = 5,width=30)
	B1 = tkinter.Button(top,text="Enter Url",command = take_new_url,width = 20)

	L1.grid(row=0, column=1)
	E1.grid(row=0, column=2)
	B1.grid(row=1, column=1)

	top.mainloop()


if not args.inputsource:
	args.inputsource = input("Take input from File/current user input. choices - file/cli . <::")

if args.inputsource == 'file':
	bodyweight = config['PHYSIQUE']['bodyweight']
	gender = config['PHYSIQUE']['gender']
	age = config['PHYSIQUE']['age']
	height = config['PHYSIQUE']['height']
	fitness_goal = config['GOAL']['goal']
	#calorie_intake = config['CALORIE']['calorie_intake']
	protein_per_body_weight_g = config['CALORIE']['protein_per_body_weight_g']
	mealnumber = config['ROUTINE']['mealnumber']
	activity_level = config['ROUTINE']['activity_level']
	args.change_protein_per_body_pound = config['CALORIE']['change_protein_per_body_pound']

elif args.inputsource == 'cli':
	
	if not args.bodyweight:
		args.bodyweight = input("Your bodyweight in kgs/lbs. Example- 55kgs/55lbs <::")
	bodyweight = args.bodyweight
	
	if not args.age:
		args.age = input("Your age in years. Example- 21yrs <::")
	age = args.age

	if not args.gender:
		args.gender = input("Your Gender. Choices- male/female <::")
	gender = args.gender

	if not args.height:
		args.height = input("Your height in feet-inch. Example: 5ft7in . <::")
	height = args.height

	if not args.goal:
		args.goal = input("Your goal. Options - maintain/loose/gain/Lean_Bulking <::")
	fitness_goal = args.goal

	if not args.mealnumber:
		args.mealnumber = input("Number of meals you can take a day. Ex: 4-8 is a good number with proper quantity of food. <::")
	mealnumber = args.mealnumber

	activity_level_string = "Choices-\n0) Basal Metabolic Rate\n1) Little/No exercise\n2) 3 times/week\n3) 4 times/week\n4) 5 times/week\n5) Daily\n6) 5 times/week(Intense)\n7) Daily(Intense) or Twice Daily\n8) Daily exercise + Physical Job\nEnter 0-8 according to your choice. <::"
	activity_level = input(activity_level_string)


	if not args.change_protein_per_body_pound:
		args.change_protein_per_body_pound = input("Change protein bodyweight "+str(protein_per_body_weight_g)+"g?. <::")

else:
	raise ValueError('Invalid choice.')

if gender == 'male' or gender == 'female':
	pass
else:
	raise ValueError(gender+" is invalid gender. Sex can be 'male' or 'female'.")
body_weight_digit,body_weight_unit = filter_bodyweight(bodyweight)
#calorie_intake_digit,calorie_unit = filter_calorie(calorie_intake)
age_yrs,age_unit = filter_age(age)
mealnumber = filter_mealnumber(mealnumber)
feet_digit,inch_digit = filter_height_feet_inch(height)
height_cm = feet_to_cm(feet_digit) + inch_to_cm(inch_digit)
try:
	activity_level = int(activity_level)
except ValueError:
	raise ValueError(str(activity_level)+" is not integer. activity_level needs to be integer.")


if args.change_protein_per_body_pound == 'yes':
	protein_per_body_weight_g = input("Protein per body weight in grams. for muscle gain 0.5 - 1.8. For beginner 0.5. For intermediate 1. <<:")

protein_per_body_weight_g = float(protein_per_body_weight_g)
#change_protein_per_body_pound = args.change_protein_per_body_pound

activity_level_sentences = ['Basal Metabolic Rate','Little/No exercise','3 times/week','4 times/week','5 times/week','Daily','5 times/week(Intense)','Daily(Intense) or Twice Daily','Daily exercise + Physical Job']

print("\nGiven,")
print("	Your Goal: "+fitness_goal)
print("	Your Gender: "+gender)
print("	Your Age: "+str(age_yrs)+" years")
print("	Your Height: "+str(feet_digit)+" feet "+str(inch_digit)+" inch")
print("	Your Bodyweight = "+str(body_weight_digit) + " " + body_weight_unit)
print("	Your Mealnumber: "+str(mealnumber))
print("	Your Activity Level: "+activity_level_sentences[activity_level])

print("	Your Daily Protein requirement per bodyweight according to goal: "+str(protein_per_body_weight_g)+"g")

if body_weight_unit == 'kgs':
	body_weight_digit = kgs_to_lbs(body_weight_digit)
	body_weight_unit = 'lbs'

bodyweight_kgs = lbs_to_kgs(body_weight_digit)
BMR = bmr(gender,bodyweight_kgs,height_cm,age_yrs)

maintenance_calorie_intake = Maintenance_Calories_Per_Day(BMR,activity_level)
lean_gaining_calorie_intake = int(maintenance_calorie_intake + maintenance_calorie_intake*(10/100))
gaining_calorie_intake = int(maintenance_calorie_intake + maintenance_calorie_intake*(20/100))
cutting_calorie_intake = int(maintenance_calorie_intake - maintenance_calorie_intake*(20/100))
extreme_cutting_calorie_intake = int(maintenance_calorie_intake - maintenance_calorie_intake*(40/100))

if fitness_goal == 'maintain':
	calorie_intake = maintenance_calorie_intake
elif fitness_goal == 'gain':
	calorie_intake = gaining_calorie_intake
elif fitness_goal == 'Lean_Bulking':
	## ***Need low fat lean body so that we can measure body weight for protein / body weight, which can be intaked for max muscle maintance
	calorie_intake = lean_gaining_calorie_intake
elif args.goal == 'loose':
	calorie_intake = cutting_calorie_intake
elif args.goal == 'extra_loose':
	calorie_intake = cutting_calorie_intake
	

fat_percentage_relative_to_protein = 0.4

## kcal unit
protein_energy_per_g = 4.0
fat_energy_per_g = 9.0
carbohydrate_energy_per_g = 4.0

protein_requirement_g = body_weight_digit*protein_per_body_weight_g
protein_energy = protein_requirement_g*protein_energy_per_g
fat_requirement_g = protein_requirement_g*fat_percentage_relative_to_protein
fat_energy = fat_requirement_g*fat_energy_per_g
carbohydrate_energy = calorie_intake - (protein_energy + fat_energy)
carbohydrate_requirement_g = carbohydrate_energy/4

per_meal_protein_requirement_g = protein_requirement_g/mealnumber
per_meal_fat_requirement_g = fat_requirement_g/mealnumber
per_meal_carbohydrate_requirement_g = carbohydrate_requirement_g/mealnumber

print("Result,")
print("  Your Daily CALORIE intake: "+str(calorie_intake)+"Kcal")
print("  Your Daily Macros - "+str(round(protein_requirement_g,2))+"g Protein|"+str(round(fat_requirement_g,2))+"g Fat|"+str(round(carbohydrate_requirement_g,2))+"g Carbohydrate")
print("  Your need to eat per meal - "+str(round(per_meal_protein_requirement_g,2))+"g Protein|"+str(round(per_meal_fat_requirement_g,2))+"g Fat|"+str(round(per_meal_carbohydrate_requirement_g,2))+"g Carbohydrate")


next_step = input("\nWant next step ?:")
if next_step == "yes":
	print("Cook & Pack your foods into "+str(mealnumber)+" food containers. Each container will contain "+str(round(per_meal_protein_requirement_g,2))+"g Protein|"+str(round(per_meal_fat_requirement_g,2))+"g Fat|"+str(round(per_meal_carbohydrate_requirement_g,2))+"g Carbohydrate")