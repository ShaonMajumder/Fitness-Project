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
	#Check or ignore or re-evaluate above

	""" Followiing now : Mifflin-St Jeor """
	### Calorie Calculator - https://www.freedieting.com/calorie-calculator
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

def filter_activity_level(activity_level):
	try:
		activity_level = int(activity_level)
	except ValueError:
		raise ValueError(str(activity_level)+" is not integer. activity_level needs to be integer.")
	return activity_level

def filter_protein_grams_per_body_pound(protein_grams_per_body_pound):
	protein_grams_per_body_pound = float(protein_grams_per_body_pound)
	if( protein_grams_per_body_pound > 1.5 ):
		raise ValueError("You are consuming too much protein for per body pound !!!")
	elif(protein_grams_per_body_pound < 0.5 ):
		raise ValueError("You are consuming too less protein for per body pound !!!")
	return protein_grams_per_body_pound

def nutrition_calculator(gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal,debug=False):
	activity_level_sentences = ['Basal Metabolic Rate','Little/No exercise','3 times/week','4 times/week','5 times/week','Daily','5 times/week(Intense)','Daily(Intense) or Twice Daily','Daily exercise + Physical Job']
	
	body_weight_digit,body_weight_unit = filter_bodyweight(bodyweight)
	#calorie_intake_digit,calorie_unit = filter_calorie(calorie_intake)
	age_yrs,age_unit = filter_age(age)
	mealnumber = filter_mealnumber(mealnumber)
	feet_digit,inch_digit = filter_height_feet_inch(height)
	height_cm = feet_to_cm(feet_digit) + inch_to_cm(inch_digit)
	activity_level = filter_activity_level(activity_level)
	protein_grams_per_body_pound = filter_protein_grams_per_body_pound(protein_grams_per_body_pound)

	print_stri = f"""Given yours,\n  Goal: {fitness_goal}\n  Gender: {gender}\n  Age: {age_yrs} years\n  Height: {feet_digit} feet {inch_digit} inch\n  Bodyweight = {body_weight_digit} {body_weight_unit}\n  Daily Mealnumber: {mealnumber}\n  Daily Activity Level: {activity_level_sentences[activity_level]}\n  According to goal,\n  Daily Protein requirement per body pound: {protein_grams_per_body_pound} grams"""
	if(debug): print(print_stri)
	
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

	protein_requirement_g = body_weight_digit*protein_grams_per_body_pound
	protein_energy = protein_requirement_g*protein_energy_per_g
	fat_requirement_g = protein_requirement_g*fat_percentage_relative_to_protein
	fat_energy = fat_requirement_g*fat_energy_per_g
	carbohydrate_energy = calorie_intake - (protein_energy + fat_energy)
	carbohydrate_requirement_g = carbohydrate_energy/4

	per_meal_protein_requirement_g = protein_requirement_g/mealnumber
	per_meal_fat_requirement_g = fat_requirement_g/mealnumber
	per_meal_carbohydrate_requirement_g = carbohydrate_requirement_g/mealnumber

	return calorie_intake,protein_requirement_g,carbohydrate_requirement_g,fat_requirement_g,per_meal_protein_requirement_g,per_meal_carbohydrate_requirement_g,per_meal_fat_requirement_g
