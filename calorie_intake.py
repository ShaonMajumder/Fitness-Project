import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--bodyweight",help="Your bodyweight in kgs/lbs. Example: 30kgs or 30lbs",type=str)
parser.add_argument("--goal", choices=['maintain', 'gain', 'loose'],help="'maintain' for maintaining your current body mass/'loose' for loosing body fat/'gain' for gaining muscle")
args = parser.parse_args()

def kgs_to_lbs(kgs):
	unit_kg_to_pound = 2.20462
	return kgs*unit_kg_to_pound

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

if not args.bodyweight:
	args.bodyweight = input("Your bodyweight in kgs/lbs. Example- 55kgs/55lbs <::")
body_weight_digit,body_weight_unit = filter_bodyweight(args.bodyweight)

print("Bodyweight = "+str(body_weight_digit) + " " + body_weight_unit)

if not args.goal:
	args.goal = input("Your goal. Options - maintain/loose/gain <::")

print("Your Goal: "+args.goal)

if args.goal == 'maintain':
	## ***Need low fat lean body so that we can measure body weight for protein / body weight, which can be intaked for max muscle maintance
	maintainance_calorie = float(input("Your maintainance calorie in number(unit Kcal) <::"))
	if body_weight_unit == 'kgs':
		body_weight_digit = kgs_to_lbs(body_weight_digit)
		body_weight_unit = 'lbs'

	protein_per_body_weight_g = 1.0
	poption = input("Do you want to change protein per bodyweight= "+str(protein_per_body_weight_g)+"gram? Option:yes/no <::")
	if(poption == "yes"):
		protein_per_body_weight_g = float(input("Your protien intake per bodyweight in grams <::"))
	elif(poption == "no"):
		pass
	else:
		raise ValueError("invalid input")

	fat_percentage_relative_to_protein = 0.4
	
	## kcal unit
	protein_energy_per_g = 4.0
	fat_energy_per_g = 9.0
	carbohydrate_energy_per_g = 4.0

	protein_requirement_g = body_weight_digit*protein_per_body_weight_g
	protein_energy = protein_requirement_g*protein_energy_per_g
	fat_requirement_g = protein_requirement_g*fat_percentage_relative_to_protein
	fat_energy = fat_requirement_g*fat_energy_per_g
	carbohydrate_energy = maintainance_calorie - (protein_energy + fat_energy)
	carbohydrate_requirement_g = carbohydrate_energy/4


	print("Your Macros - "+str(protein_requirement_g)+" Protein|"+str(fat_requirement_g)+" Fat|"+str(carbohydrate_requirement_g)+" Carbohydrate")

elif args.goal == 'gain':
	pass
elif args.goal == 'loose':
	pass
