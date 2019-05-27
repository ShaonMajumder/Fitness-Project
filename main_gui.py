# -*- coding: utf-8 -*-
#https://www.freedieting.com/calorie-calculator
# (Routine Consistency & Soldier & Monk Mind)
# Goal - & Work & Stress planning
# Sleep >
# Exercise >
# Nutrition according to goal and exercise, work, stress >
# Hygene >
# Identity & Carrier execution >
# Social health

"""
User_Profile_Frame         Sleep_Section_Frame        | Goal Section
Exercise_Section_Frame     Nutrition_Section_Frame 	  | Day Planning Section
Hygene_Section_Frame       Grooming_Section_Frame 	  | Social Section
"""
Muscles = ['Deltoids','Triceps','Biceps','Forearm','Trapezius','Middle Back','Latissimus Dorsi','Lower Back','Quadriceps','Calves','Hamstring','Upper Abs','Lower Abs','Obliques']
def create_new_profile():
	print(randomString(stringLength=8))
from imports import *
config = read_config_ini("safe_directory/dbconfig.ini")
datetime_ = datetime.now().strftime("%d/%m/%y")

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

time_units = ['years','months','days','hours','minutes','seconds']
time_quan = {'seconds':60, 'minutes':60, 'hours':24, 'days':30, 'months':12, 'years':1}

"""
Nutrition Functions
"""
def add_shopping_list_to_inventory(food_name,food_quantity_digit,food_quantity_unit):
	"""
	Converting Purchasing_Unit
	kg,grams = kg,grams_to_kg #Actual_unit_weight_grams in grams after peeling and cleaning
	piece,hali,dozen = piece,hali_to_piece,dozen_to_piece
	bundle = bundle
	litre = litre
	OPTIONS_Food_Unit = ['kg','gram','piece','hali','dozen','bundle','litre']
	#unique = kg,bundle,litre,piece
	"""
	if food_quantity_unit == 'gram':
		food_quantity_digit = gram_to_kg(food_quantity_digit)
		food_quantity_unit = 'kg'
	elif food_quantity_unit == 'hali':
		food_quantity_digit = hali_to_piece(food_quantity_digit)
		food_quantity_unit = 'piece'
	elif food_quantity_unit == 'dozen':
		food_quantity_digit = dozen_to_piece(food_quantity_digit)
		food_quantity_unit = 'piece'

	results = mydb.select(['Food_Id','Purchasing_Unit','Actual_unit_weight_grams'], f"""`Name`='{food_name}'""" ,'nutrition_values')
	Food_Id = results[0]['Food_Id']
	Purchasing_Unit = results[0]['Purchasing_Unit']
	
	if food_quantity_unit == 'piece':
		actual_Unit_weight = results[0]['Actual_unit_weight_grams']
	if food_quantity_unit == 'kg':
		actual_Unit_weight = results[0]['Actual_unit_weight_grams']
	weight = float(actual_Unit_weight)*food_quantity_digit

	results = mydb.select(['Food_Id','quantity','unit'],f"""`Food_Id` = '{Food_Id}'""","food_inventory")
	if results == ():
		mydb.insert(['Food_Id','food_name','quantity','unit','weight'],[Food_Id,food_name,food_quantity_digit,food_quantity_unit,weight],'food_inventory')
	else:
		#add the quantity
		row = results[0]
		quantity = float(row['quantity'])

		if row['unit'] == food_quantity_unit:
			quantity = food_quantity_digit + quantity
			weight = float(actual_Unit_weight)*quantity
			quantity = str(quantity)
			
			mydb.edit(['quantity','weight'],[quantity,weight],f"""`Food_Id` = '{Food_Id}'""","food_inventory")

class MyDialog:
    def __init__(self, parent):

        top = self.top = tkinter.Toplevel(parent)

        tkinter.Label(top, text="Value").pack()

        self.e = tkinter.Entry(top)
        self.e.pack(padx=5)
        self.e.focus_set()
        self.e.bind('<Return>', self.ok)

        b = tkinter.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)        

    def ok(self,event):
        self.value = self.e.get()
        self.top.destroy()




## Main 

def app_frame_loop():
	global top_frame
	top_frame = tkinter.Tk()
	top_frame.tk.call('encoding', 'system', 'utf-8')
	top_frame.title("Project-Super-Human")
	top_frame.geometry("1000x800")

	draw_app_frames()
	top_frame.mainloop()


"""

user_calculation_frame = tkinter.Frame(top_frame, bg = 'blue', relief=tkinter.RAISED, borderwidth=1)
user_calculation_frame.grid(sticky="W", row = 2, column = 0)


Todays_Calorie_Need_Label = 
Total_Calorie_Need_Label =
Todays_Consumable_Ammount_Label =
"""


#Date_Label = tkinter.Label(user_profile_frame, text = "Date")

"""
user_calculation_frame_Label = tkinter.Label(user_calculation_frame, text = "Calculated Section")
Previus_Calorie_Surplus_Deficit_Label = tkinter.Label(user_calculation_frame, text = "Previous Day Calorie Surplus or Deficit")
#Depends on goal if you have to remain in surplus and deficit, then calculate todays calorie cut or add
#calculate metabolism rate to get extra amount you can consume
Todays_Highest_Calorie_Allowed_cutting_or_adding_for_meeting_surplus_or_deficit_Label = tkinter.Label(user_calculation_frame, text = "Highest Calorie to cut or add")
# minus if you are in extra calorie surplus
Todays_Calorie_Need_Label = tkinter.Label(user_calculation_frame, text = "Todays Calorie Need")
Daily_Macro_Split_Label = tkinter.Label(user_calculation_frame, text = "Todays Macro Split")
PerMeal_Spit = tkinter.Label(user_calculation_frame, text = "Details Meal Description(Day Heavy, night Light) -")
"""




"""
level_row = 3
Date_Label.grid(sticky="W", row=level_row, column=1)
Gender_Label.grid(sticky="W", row=level_row + 1, column=1)
Goal_Label.grid(sticky="W", row=level_row + 2, column=1)
Goal_D.grid(sticky="W", row=level_row + 2, column=2)
#Tip: Calculate extra rep set in next day
Age_Label.grid(sticky="W", row=level_row + 3, column=1)
Height_Label.grid(sticky="W", row=level_row + 4, column=1)
Bodyweight_Label.grid(sticky="W", row=level_row + 5, column=1)
Body_Fat_Percentage_Label.grid(sticky="W", row=level_row + 6, column=1)
Blood_Pressure_Label.grid(sticky="W", row=level_row + 7, column=1)
Meal_Number_Label.grid(sticky="W", row=level_row + 8, column=1)
Fasting_Day_Label.grid(sticky="W", row=level_row + 9, column=1)
"""

"""
user_calculation_frame_Label.grid(sticky="W", row=1, column=1, pady=10)
Todays_Highest_Calorie_Allowed_cutting_or_adding_for_meeting_surplus_or_deficit_Label.grid(sticky="W", row=2, column=1)
Previus_Calorie_Surplus_Deficit_Label.grid(sticky="W", row=3, column=1)
#calculated according to goal and metabolism
Todays_Calorie_Need_Label.grid(sticky="W", row=4, column=1)
Daily_Macro_Split_Label.grid(sticky="W", row=5, column=1)
#BMR and RM of exercise and activity
PerMeal_Spit.grid(sticky="W", row=6, column=1)
"""

#Date_Label.grid(sticky="W", row=level_row, column=1)


def draw_user_profile_frame():
	global User_Profile_Frame
	User_Profile_Frame = tkinter.Frame(Life_Frame, bg = '#d37e7e', relief=tkinter.RAISED, borderwidth=1)
	User_Profile_Label_Color = '#e2c3c3'
	User_Profile_Frame_Label = tkinter.Label(User_Profile_Frame, bg=User_Profile_Label_Color, text = "User Profile Section")
	Gender_Label = tkinter.Label(User_Profile_Frame, bg=User_Profile_Label_Color, text = "Gender")
	Fitness_Goal_Label = tkinter.Label(User_Profile_Frame, bg=User_Profile_Label_Color, text = "Fitness Goal")
	Fitness_Goal_OPTIONS = ['Lean Bulking','Maintain','Gain','Cut']
	Fitness_Goal_category = tkinter.StringVar(User_Profile_Frame)
	Fitness_Goal_category.set(Fitness_Goal_OPTIONS[0]) # default value
	Fitness_Goal_D = tkinter.OptionMenu(User_Profile_Frame, Fitness_Goal_category, *Fitness_Goal_OPTIONS)
	Age_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Age")
	Height_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Height")
	Goal_Body_Fat_Percentage_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Goal Body Fat Percentage")
	Bodyweight_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Todays Bodyweight")
	Body_Fat_Percentage_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Todays Body Fat Percentage")
	Blood_Pressure_Label = tkinter.Label(User_Profile_Frame,bg=User_Profile_Label_Color, text = "Todays Blood Pressure")

	level_row = 3
	User_Profile_Frame.grid(sticky="W", row = 1, column = 1)
	User_Profile_Frame_Label.grid(sticky="W", row = 1, column = 1)
	Gender_Label.grid(sticky="W", row=level_row + 1, column=1)
	Fitness_Goal_Label.grid(sticky="W", row=level_row + 2, column=1)
	Fitness_Goal_D.grid(sticky="W", row=level_row + 2, column=2)
	#Tip: Calculate extra rep set in next day
	Age_Label.grid(sticky="W", row=level_row + 3, column=1)
	Height_Label.grid(sticky="W", row=level_row + 4, column=1)
	Goal_Body_Fat_Percentage_Label.grid(sticky="W", row=level_row + 5, column=1)
	Bodyweight_Label.grid(sticky="W", row=level_row + 6, column=1)
	Body_Fat_Percentage_Label.grid(sticky="W", row=level_row + 7, column=1)
	Blood_Pressure_Label.grid(sticky="W", row=level_row + 8, column=1)

def draw_nutrition_section_frame():
	global Nutrition_Section_Frame
	Nutrition_Section_Frame = tkinter.Frame(Life_Frame, bg = 'blue', relief=tkinter.RAISED, borderwidth=1)
	Nutrition_Section_Frame_Label = tkinter.Label(Nutrition_Section_Frame, text = "Nutrition Section")
	Nutrition_Section_Open_Button = tkinter.Button(Nutrition_Section_Frame, text = "Open", command=nutrition_form)
	Nutrition_Section_Frame.grid(sticky="W", row = 2, column = 2)
	Nutrition_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)
	Nutrition_Section_Open_Button.grid(sticky="W", row = 1, column = 2)

def draw_hygene_section_frame():
	global Hygene_Section_Frame
	Hygene_Section_Frame = tkinter.Frame(Life_Frame, bg = 'yellow', relief=tkinter.RAISED, borderwidth=1)
	Hygene_Section_Frame_Label = tkinter.Label(Hygene_Section_Frame, text = "Hygene Section")
	Penis_Hygene_Label = tkinter.Label(Hygene_Section_Frame, text = "Penis Hygene")
	Unnecessary_Hair_Removal_Label = tkinter.Label(Hygene_Section_Frame, text = "Unnecessary Hair Removal")
	Bactrial_Smell_Body_Spray_Label = tkinter.Label(Hygene_Section_Frame, text = "Bactrial Smell Body Spray")
	Hair_Smell_Label = tkinter.Label(Hygene_Section_Frame, text = "Hair Smell Spray")
	Bath_Label = tkinter.Label(Hygene_Section_Frame, text = "Bath")
	Teeth_Brush_Label = tkinter.Label(Hygene_Section_Frame, text = "Teeth Brush")
	Shampoo_Label = tkinter.Label(Hygene_Section_Frame, text = "Shampoo")
	Hair_Cut_Label = tkinter.Label(Hygene_Section_Frame, text = "Hair Cut")
	Nail_Cut_Label = tkinter.Label(Hygene_Section_Frame, text = "Nail Cut")

	Hygene_Section_Frame.grid(sticky="W", row = 3, column = 1)
	Hygene_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)
	Penis_Hygene_Label.grid(sticky="W", row = 2, column = 1)
	Unnecessary_Hair_Removal_Label.grid(sticky="W", row = 3, column = 1)
	Bactrial_Smell_Body_Spray_Label.grid(sticky="W", row = 4, column = 1)
	Hair_Smell_Label.grid(sticky="W", row = 5, column = 1)
	Bath_Label.grid(sticky="W", row = 6, column = 1)
	Teeth_Brush_Label.grid(sticky="W", row = 7, column = 1)
	Shampoo_Label.grid(sticky="W", row = 8, column = 1)
	Hair_Cut_Label.grid(sticky="W", row = 9, column = 1)
	Nail_Cut_Label.grid(sticky="W", row = 10, column = 1)

def draw_grooming_section_frame():
	global Grooming_Section_Frame
	Grooming_Section_Frame = tkinter.Frame(Life_Frame, bg = 'violet', relief=tkinter.RAISED, borderwidth=1)
	Grooming_Section_Frame_Label = tkinter.Label(Grooming_Section_Frame, text = "Grooming Section")
	Grooming_Section_Frame.grid(sticky="W", row = 3, column = 2)
	Grooming_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)

def draw_goal_section_frame():
	global Goal_Section_Frame
	Goal_Section_Frame = tkinter.Frame(Corporate_Frame, bg = 'orange', relief=tkinter.RAISED, borderwidth=1)
	Goal_Section_Frame_Label = tkinter.Label(Goal_Section_Frame, text = "Goal Section")
	Goal_Section_Frame.grid(sticky="w",row=1,column=1)
	Goal_Section_Frame_Label.grid(sticky="w",row=1,column=1)
def draw_day_planning_section_frame():
	global Day_Planning_Section_Frame
	Day_Planning_Section_Frame = tkinter.Frame(Corporate_Frame, bg = 'blue', relief=tkinter.RAISED, borderwidth=1)
	Day_Planning_Section_Frame_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Day Planning Section")
	Day_Planning_Section_Frame_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Important")
	Day_Planning_Section_Frame_Not_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Not Important")
	Day_Planning_Section_Frame_Now_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Now")
	Day_Planning_Section_Frame_Later_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Later")
	Day_Planning_Section_First_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
	Day_Planning_Section_Second_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
	Day_Planning_Section_Third_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
	Day_Planning_Section_Fourth_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')

	Day_Planning_Section_Frame.grid(sticky="w",row=2,column=1)
	Day_Planning_Section_Frame_Label.grid(sticky="w",row=1,column=1)

	Day_Planning_Section_First_Grid.grid(sticky="w",row=3,column=2)
	Day_Planning_Section_Second_Grid.grid(sticky="w",row=3,column=3)
	Day_Planning_Section_Third_Grid.grid(sticky="w",row=4,column=2)
	Day_Planning_Section_Fourth_Grid.grid(sticky="w",row=4,column=3)

	Day_Planning_Section_Frame_Important_Label.grid(sticky="w",row=3,column=1)
	Day_Planning_Section_Frame_Not_Important_Label.grid(sticky="w",row=4,column=1)
	Day_Planning_Section_Frame_Now_Important_Label.grid(sticky="w",row=2,column=2)
	Day_Planning_Section_Frame_Later_Important_Label.grid(sticky="w",row=2,column=3)

def draw_social_section_frame():
	global Social_Section_Frame
	Social_Section_Frame = tkinter.Frame(Corporate_Frame, bg = 'green', relief=tkinter.RAISED, borderwidth=1)
	Social_Section_Frame_Label = tkinter.Label(Social_Section_Frame, text = "Social Section")
	Social_Section_Frame.grid(sticky="w",row=3,column=1)
	Social_Section_Frame_Label.grid(sticky="w",row=1,column=1)

def draw_app_frames():
	global Life_Frame
	Life_Frame = tkinter.Frame(top_frame, bg = 'indigo', relief=tkinter.RAISED, borderwidth=1)
	Life_Frame.grid(sticky = 'W', row = 1, column = 1)

	global Corporate_Frame
	Corporate_Frame = tkinter.Frame(top_frame, bg = 'indigo', relief=tkinter.RAISED, borderwidth=1)
	Corporate_Frame.grid(sticky = 'W', row = 1, column = 2)

	draw_user_profile_frame()
	
	draw_nutrition_section_frame()	
	draw_hygene_section_frame()
	draw_grooming_section_frame()
	draw_goal_section_frame()
	draw_day_planning_section_frame()
	draw_social_section_frame()






	


def nutrition_form():
	# Main - f0f0f0
	#mydb.delete_table('nutrition_values')
	#mydb.import_from_xlsx('safe_directory/nutrition_values.xlsx','nutrition_values')

	def plan_meal_form():
		Plan_Meal_Form = tkinter.Toplevel(Nutrition_Registry_Form)
		Plan_Meal_Form.geometry("600x400")
		Plan_Meal_Form.title("Plan Meal")

		Meal_Number_Label = tkinter.Label(Plan_Meal_Form, text = "Meal Number")
		Fasting_Day_Label = tkinter.Label(Plan_Meal_Form, text = "Fasting Day")
		Food_Name_Label = tkinter.Label(Plan_Meal_Form, text = "Food Name-")
		Food_Quantity_Label = tkinter.Label(Plan_Meal_Form, text = "Quantity-")

		Meal_Number_Label.grid(sticky="W", row=1, column=1)
		Fasting_Day_Label.grid(sticky="W", row=2, column=1)
		Food_Name_Label.grid(sticky="W", row=3, column=1)
		Food_Quantity_Label.grid(sticky="W", row=3, column=2)


	def manage_inventory_form():
		def add_to_inventory():
			food_name = MANAGE_INVENTORY_Food_Name_Entry.get()
			food_quantity_digit = float(MANAGE_INVENTORY_Food_Consumed_Quantity_Entry.get())
			food_quantity_unit = OptionsVar_Food_Unit.get()
			add_shopping_list_to_inventory(food_name,food_quantity_digit,food_quantity_unit)
			MANAGE_INVENTORY_FORM.destroy()

		MANAGE_INVENTORY_FORM = tkinter.Toplevel(top_frame)
		MANAGE_INVENTORY_FORM.geometry("600x400")
		MANAGE_INVENTORY_FORM.title("Manage Inventory")
		MANAGE_INVENTORY_Food_Name_Label = tkinter.Label(MANAGE_INVENTORY_FORM, text="Food Name", bg="white")

		result= mydb.select(['Name','Bangla_Name'],"","nutrition_values")
		Food_list = [line['Name'] for line in result]
		MANAGE_INVENTORY_Food_Name_Entry = AutocompleteEntry(Food_list, MANAGE_INVENTORY_FORM, bd = 2, width=30)	
		MANAGE_INVENTORY_Food_Consumed_Quantity_Label = tkinter.Label(MANAGE_INVENTORY_FORM, text="Quantity", bg="white")
		MANAGE_INVENTORY_Food_Consumed_Quantity_Entry = tkinter.Entry(MANAGE_INVENTORY_FORM,width=12)

		OptionsVar_Food_Unit = tkinter.StringVar(MANAGE_INVENTORY_FORM)
		OPTIONS_Food_Unit = ['kg','gram','piece','hali','dozen','bundle','litre']
		OptionsVar_Food_Unit.set(OPTIONS_Food_Unit[0])
		MANAGE_INVENTORY_Food_Consumed_Quantity_Option = tkinter.OptionMenu(MANAGE_INVENTORY_FORM, OptionsVar_Food_Unit, *OPTIONS_Food_Unit)
		MANAGE_INVENTORY_ADD_TO_INVENTORY_Button = tkinter.Button(MANAGE_INVENTORY_FORM, text = "Add to Inventory", bg='white', command=add_to_inventory)

		MANAGE_INVENTORY_Food_Name_Label.grid(sticky="w",row=1,column=1)
		MANAGE_INVENTORY_Food_Name_Entry.grid(sticky="w",row=1,column=2)
		MANAGE_INVENTORY_Food_Consumed_Quantity_Label.grid(sticky="w",row=1,column=3)
		MANAGE_INVENTORY_Food_Consumed_Quantity_Entry.grid(sticky="w",row=1,column=4)
		MANAGE_INVENTORY_Food_Consumed_Quantity_Option.grid(sticky="w",row=1,column=5)
		MANAGE_INVENTORY_ADD_TO_INVENTORY_Button.grid(sticky="w",row=2,column=1)

	def record_unplanned_meal_form():
		def record_unplanned_meal_submit_add_new():
			record_unplanned_meal_submit(True)
		def record_unplanned_meal_submit(add_new=False):
			today = date.today()#Highlight in form
			food_name = Record_Unplanned_Meal_Food_Name_Entry.get()
			number = Record_Unplanned_Meal_Food_Consumed_Quantity_Number.get()
			unit= OptionsVar_Food_Unit.get()
			
			#add previous
			result = mydb.select(['id','food_name','number','unit'],"`date` = '"+str(today)+"' and `food_name`='"+food_name+"'",'nutrition_record')
			if result == ():
				mydb.insert(['date','food_name','number','unit'],[today,food_name,number,unit],'nutrition_record')
			else:
				result = result[0]
				if result['unit'] == unit:
					number = str(float(result['number'])+float(number))
					mydb.edit(['number'],[number],"`id`="+str(result['id']),'nutrition_record')


			if(add_new):
				Record_Unplanned_Meal_Form.destroy()
			else:
				#record_unplanned_meal_form()
				Record_Unplanned_Meal_Form.destroy()


		result= mydb.select(['Name','Bangla_Name'],"","nutrition_values")
		Food_list = [line['Name'] for line in result]

		Record_Unplanned_Meal_Form = tkinter.Toplevel(top_frame)
		Record_Unplanned_Meal_Form.geometry("600x400")
		Record_Unplanned_Meal_Form.title("Record Unplanned Meal")
		Record_Unplanned_Meal_Food_Date_Label = tkinter.Label(Record_Unplanned_Meal_Form, text="Date - "+str(date.today()), bg="white")
		Record_Unplanned_Meal_Food_Name_Label = tkinter.Label(Record_Unplanned_Meal_Form, text="Food Name", bg="white")
		Record_Unplanned_Meal_Food_Name_Entry = AutocompleteEntry(Food_list, Record_Unplanned_Meal_Form, bd = 2, width=30)	
		Record_Unplanned_Meal_Food_Consumed_Quantity_Label = tkinter.Label(Record_Unplanned_Meal_Form, text="Consumed Quantity", bg="white")
		
		OptionsVar_Food_Unit = tkinter.StringVar(Record_Unplanned_Meal_Form)
		OPTIONS_Food_Unit = ['piece','spoon','palm','bowl','gram','litre']
		OptionsVar_Food_Unit.set(OPTIONS_Food_Unit[0])
		Record_Unplanned_Meal_Food_Consumed_Quantity_Option = tkinter.OptionMenu(Record_Unplanned_Meal_Form, OptionsVar_Food_Unit, *OPTIONS_Food_Unit, command = select_category_action)
		


		#appHighlightFont = font.Font(family='Helvetica', size=12, weight='bold')
		#print(font.families())

		Record_Unplanned_Meal_Food_Consumed_Quantity_Number = tkinter.Entry(Record_Unplanned_Meal_Form,width=12,exportselection=0)
		Record_Unplanned_Meal_Food_Submit_Button = tkinter.Button(Record_Unplanned_Meal_Form, text = "Submit", bg='white', command=record_unplanned_meal_submit)
		Record_Unplanned_Meal_Food_Submit_And_Add_New_Button = tkinter.Button(Record_Unplanned_Meal_Form, text = "Submit and Add New", bg='white', command=record_unplanned_meal_submit_add_new)
		
		Record_Unplanned_Meal_Food_Date_Label.grid(sticky="w",row=0,column=1)
		Record_Unplanned_Meal_Food_Name_Label.grid(sticky="w",row=1,column=1)
		Record_Unplanned_Meal_Food_Name_Entry.grid(sticky="w",row=1,column=2)
		Record_Unplanned_Meal_Food_Consumed_Quantity_Label.grid(sticky="w",row=1,column=3)		
		Record_Unplanned_Meal_Food_Consumed_Quantity_Number.grid(sticky="w",row=1,column=4)
		Record_Unplanned_Meal_Food_Consumed_Quantity_Option.grid(sticky="w",row=1,column=5)
		Record_Unplanned_Meal_Food_Submit_Button.grid(sticky="w",row=2,column=1)
		Record_Unplanned_Meal_Food_Submit_And_Add_New_Button.grid(sticky="w",row=2,column=2)

	Nutrition_Registry_Form = tkinter.Toplevel(top_frame)
	Nutrition_Registry_Form.geometry("400x400")
	Nutrition_Registry_Form.title("Nutrition Form")
	Nutrition_Section_Form_Label = tkinter.Label(Nutrition_Registry_Form, text = "Nutrition Section", bg="white")
	Nutrition_Form_Label_Color = 'white'
	Nutrition_Section_Record_Unplanned_Meal_Label = tkinter.Button(Nutrition_Registry_Form, text = "Record Unplanned Meal", bg=Nutrition_Form_Label_Color, command=record_unplanned_meal_form)
	Nutrition_Section_Plan_Meal_Label = tkinter.Button(Nutrition_Registry_Form, text = "Plan Meal", bg=Nutrition_Form_Label_Color, command=plan_meal_form)
	Nutrition_Section_Manage_Inventory_Label = tkinter.Button(Nutrition_Registry_Form, text = "Manage Inventory", bg=Nutrition_Form_Label_Color, command=manage_inventory_form)
	Nutrition_Section_Add_New_Food_Label = tkinter.Button(Nutrition_Registry_Form, text = "Record New Food", bg=Nutrition_Form_Label_Color)

	Nutrition_Section_Form_Label.grid(sticky="w",row=1,column=1)
	Nutrition_Section_Record_Unplanned_Meal_Label.grid(sticky="w",row=2,column=1)
	Nutrition_Section_Plan_Meal_Label.grid(sticky="w",row=3,column=1)
	Nutrition_Section_Manage_Inventory_Label.grid(sticky="w",row=4,column=1)
	Nutrition_Section_Add_New_Food_Label.grid(sticky="w",row=5,column=1)


app_frame_loop()
