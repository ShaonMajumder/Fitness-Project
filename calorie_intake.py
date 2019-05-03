### Calorie Calculator - https://www.freedieting.com/calorie-calculator
### Katch-McArdle Formula: Enter Body Fat % 
### Body Fat Calculator - https://www.freedieting.com/body-fat-calculator
### Find food requirement based on Body fat percentage, learn how to measure body fat percentage
### Muscle Tape - https://www.daraz.com.bd/products/te-1-pc-simple-cnvenient-body-tape-measure-for-measuring-waist-diet-weight-loss-i103024775-s1017430360.html?spm=a2a0e.searchlist.list.7.77282e39nkmCcz&search=1
### Fat Caliper - https://www.daraz.com.bd/catalog/?q=fat+caliper
### bmr activity multiplier for weight lifters
### Body fat% for 6 pack calculation - https://www.youtube.com/watch?v=j4zOuCYYCcs

from utilities.science import *
from utilities.utility import *
import argparse

def cli_input_sequence():
	parser = argparse.ArgumentParser()
	parser.add_argument("--inputsource", choices=['file', 'cli'], help="file - For take input saved from file.\ncli - for take inputs from argument or prompt. If not specified it takes from file.",type=str)
	parser.add_argument("--bodyweight", help="Your bodyweight in kgs/lbs. Example: 60kgs or 60lbs",type=str)
	parser.add_argument("--age", help="Your age in years. Example: 20yrs",type=str)
	parser.add_argument("--gender", choices=['male', 'female'], help="Your gender. Example: male/female",type=str)
	parser.add_argument("--height", help="Your height in feet-inch. Example: 5ft7in",type=str)
	parser.add_argument("--goal", choices=['maintain','Lean_Bulking', 'gain', 'loose'], help="'Lean Bulking' for gaining muscle and cutting body fat at the same time. maintain' for maintaining your current body mass/'loose' for loosing body fat/'gain' for gaining muscle")
	parser.add_argument("--mealnumber",help="Number of meals you can take a day. Ex: 4-8 is a good number with proper quantity of food.",type=str)
	#parser.add_argument("--calorie_intake",help="Daily CALORIE amount in Kcal.",type=str)
	parser.add_argument("--change_protein_grams_per_body_pound",help="change_protein_grams_per_body_pound.",type=str)
	args = parser.parse_args()


	if not args.inputsource:
		args.inputsource = input("Take input from File/current user input. choices - file/cli . <::")

	if args.inputsource == 'cli':
		
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
		
		activity_level = input("Choices-\n0) Basal Metabolic Rate\n1) Little/No exercise\n2) 3 times/week\n3) 4 times/week\n4) 5 times/week\n5) Daily\n6) 5 times/week(Intense)\n7) Daily(Intense) or Twice Daily\n8) Daily exercise + Physical Job\nEnter 0-8 according to your choice. <::")

		if not args.change_protein_grams_per_body_pound:
			args.change_protein_grams_per_body_pound = input("Change protein bodyweight "+str(protein_grams_per_body_pound)+"g?. <::")

	elif args.inputsource == 'file':
		config =read_config_ini("Goal.data")

		gender = config['PHYSIQUE']['gender']
		age = config['PHYSIQUE']['age']
		height = config['PHYSIQUE']['height']
		bodyweight = config['PHYSIQUE']['bodyweight']
		activity_level = config['ROUTINE']['activity_level']
		protein_grams_per_body_pound = config['CALORIE']['protein_grams_per_body_pound']
		mealnumber = config['ROUTINE']['mealnumber']
		fitness_goal = config['GOAL']['goal']
		#calorie_intake = config['CALORIE']['calorie_intake']
		
		args.change_protein_grams_per_body_pound = config['CALORIE']['change_protein_grams_per_body_pound']

	else:
		raise ValueError('Invalid choice.')

	if args.change_protein_grams_per_body_pound == 'yes':
		protein_grams_per_body_pound = input("Protein per body weight in grams. for muscle gain 0.5 - 1.8. For beginner 0.5. For intermediate 1. <<:")

	return	gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal

def main():
	run_mode = input("gui/cli <<:")
	if run_mode == 'cli':
		pass
	elif run_mode == 'gui':
		pass

	gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal = cli_input_sequence()
	
	"""Sample Input"""
	"""
	## Defaults protein_grams_per_body_pound = 1.0
	gender = 'male'
	age = '22yrs'
	height = '5ft4in'
	bodyweight = '58kgs'
	activity_level = '5' #Daily medium
	protein_grams_per_body_pound = '1'
	mealnumber = '4'
	fitness_goal = 'maintain'
	"""

	"""Calculation Starts"""
	result = nutrition_calculator(gender,age,height,bodyweight,activity_level,protein_grams_per_body_pound,mealnumber,fitness_goal,debug=True)
	calorie_intake,protein_requirement_g,carbohydrate_requirement_g,fat_requirement_g,per_meal_protein_requirement_g,per_meal_carbohydrate_requirement_g,per_meal_fat_requirement_g = result
	"""Calculation Ends"""

	result_stri = f"""Result,
  Your Daily CALORIE intake: {calorie_intake} Kcal
  Your Daily Macros - {round(protein_requirement_g,2)}g Protein|{round(fat_requirement_g,2)}g Fat|{round(carbohydrate_requirement_g,2)}g Carbohydrate
  Your need to eat per meal - {round(per_meal_protein_requirement_g,2)}g Protein|{round(per_meal_fat_requirement_g,2)}g Fat|{round(per_meal_carbohydrate_requirement_g,2)}g Carbohydrate"""
	print(result_stri)

	
	""" Basic Steps """
	next_step = input("\nWant next step ?:")
	if next_step == "yes":
		print("Cook & Pack your foods into "+str(mealnumber)+" food containers. Each container will contain "+str(round(per_meal_protein_requirement_g,2))+"g Protein|"+str(round(per_meal_fat_requirement_g,2))+"g Fat|"+str(round(per_meal_carbohydrate_requirement_g,2))+"g Carbohydrate")

if __name__ == '__main__':
	main()