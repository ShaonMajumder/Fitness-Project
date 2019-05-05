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
Sleep_Section_Frame
Exercise_Section_Frame
Nutrition_Section_Frame
Hygene_Section_Frame
Grooming_Section_Frame
Social_Section_Frame
Rolling....


User_Profile_Frame         Sleep_Section_Frame       
Exercise_Section_Frame     Nutrition_Section_Frame
Hygene_Section_Frame       Grooming_Section_Frame
Social_Section_Frame

"""
from imports import *

Muscles = ['Deltoids','Triceps','Biceps','Forearm','Trapezius','Middle Back','Latissimus Dorsi','Lower Back','Quadriceps','Calves','Hamstring','Upper Abs','Lower Abs','Obliques']


datetime_ = datetime.now().strftime("%d/%m/%y")

def create_new_profile():
	print(randomString(stringLength=8))

config = read_config_ini("safe_directory/dbconfig.ini")
u_config = read_config_ini("youtube_config.ini")

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

Get_utube_title_choice = u_config['GETTING_UTUBE_VIDEO_TITLE']['GET_TITLE']
Get_utube_video_title_Input_File_Name = u_config['GETTING_UTUBE_VIDEO_TITLE']['Input_File_Name']
Get_utube_video_title_Output_File_Name = u_config['GETTING_UTUBE_VIDEO_TITLE']['Output_File_Name']
Get_utube_video_title_Show_Output = u_config['GETTING_UTUBE_VIDEO_TITLE']['Show_Output']

sort_choice = u_config['SORTING']['Sort']
sorting_tag_list = u_config['SORTING']['Tag_List'].split(',')
Sorting_Input_File_Name = u_config['SORTING']['Input_File_Name']
Sorting_Output_File_Name = u_config['SORTING']['Output_File_Name']
Sorting_Show_Output = u_config['SORTING']['Show_Output']

utube_title_seperating_flag = u_config['SETTINGS']['utube_title_seperating_flag']
utube_title_seperating_flag = utube_title_seperating_flag.replace('\'','')

time_units = ['years','months','days','hours','minutes','seconds']
time_quan = {'seconds':60, 'minutes':60, 'hours':24, 'days':30, 'months':12, 'years':1}


def get_site_title(url):
	page = get_html(url)
	YouTube_title = page.title.text.replace(" - YouTube","")
	return YouTube_title

def list_utbube_title(lines):
	#lines = read_file(filename)
	return [get_site_title(url) + utube_title_seperating_flag + url for url in lines]	

def find_tag_in_list(target_li,tag):
	return [stri for stri in target_li if tag in stri]


def sort_utube_urls_by_tag(filename,tag_list):
	titles = read_file(filename)
	sorted_li_1 = []
	sorted_li_2 = []
	sorted_li = []
	for tag in tag_list:
		for stri in titles:
			stri_ = stri.split(utube_title_seperating_flag)[0]
			if tag in stri_:
				sorted_li_1.append(stri)
			else:
				sorted_li_2.append(stri)
		sorted_li = sorted_li + sorted_li_1
		titles = sorted_li_2
		sorted_li_1 = []
		sorted_li_2 = []

	return sorted_li + titles

def umain():
	if(Get_utube_title_choice == 'Yes'):
		title_urls = list_utbube_title(Get_utube_video_title_Input_File_Name)
		if(Get_utube_video_title_Show_Output == 'Yes'):
			#if(get_utube_title_choice == 'Yes'):
			print(title_urls)
			
		title_urls = '\n'.join(title_urls)
		write_file(Sorting_Output_File_Name, title_urls,mode="w")
		

	
	
		
	
	

	if(sort_choice == 'Yes'):
		sorted_title_urls = sort_utube_urls_by_tag(Sorting_Input_File_Name,sorting_tag_list)
		if(Sorting_Show_Output == 'Yes'):
			print(sorted_title_urls)
		sorted_title_urls ='\n'.join(sorted_title_urls)
		write_file(Sorting_Output_File_Name, sorted_title_urls,mode="w")

def add_category(category):
	#query = "SELECT `value` FROM `constants` where `name` = 'Resource_Categories'"
	#search_result = mydb.select(['value'],"`name` = 'Resource_Categories'","constants")
	search_result = mydb.select(['value'],"`name` = 'Resource_Categories'","constants")

	value = [line['value'] for line in search_result][0] + ',' + category
	#query = "UPDATE `constants` SET `value` = '"+value+"' where `name` = 'Resource_Categories'"
	mydb.edit(['value'],[value],"`name` = 'Resource_Categories'","constants")

def search_resource(url):
	#query = "SELECT * FROM `data` WHERE (`resource_url` = '"+url+"')"
	search_result = mydb.select('*',"`resource_url` = '"+url+"'","data")
	return search_result



def take_new_url():
	
	#query = "INSERT INTO `tinder_bot`( `name`, `age`, `education`, `info_list`, `image`, `source_image`, `algorithm_name`, `probable_face_number`, `confidence`, `face_angle`) VALUES ('"+tinder_profile_name+"',"+str(tinder_profile_age)+",'"+tinder_profile_education+"', '"+str(tinder_profile_info_list).replace("'",'"')+"','"+image_name+"','"+src+"', '"+algorithm_name+"', "+str(faces)+", '"+str(confidence_list)+"', "+str(fangle)+")"
	resource_url = E1.get()
	if(resource_url != ''):
		resource_urls = resource_url.split('\n')
		
		allowed_resurce_urls = []
		for url in resource_urls:
			#query = "SELECT * FROM `data` WHERE (`resource_url` = '"+url+"')"
			search_result = mydb.select('*',"`resource_url` = '"+url+"'","data")

			if search_result == ():
				allowed_resurce_urls.append(url)
			else:
				messagebox.showinfo( "Hello Python", url+" alredy exists in data file.")

		titles = [get_site_title(url) for url in allowed_resurce_urls]

		for title,url in zip(titles,allowed_resurce_urls):
			#query = "INSERT INTO `data` (`title`,`resource_url`) VALUES ('"+title+"' , '"+url+"')"
			mydb.insert(['title','resource_url'],[title,url],'data')
			
		E1.set('')
	else:
		pass
	

def repair_data_file():
	lines = read_file(Get_utube_video_title_Input_File_Name)
	lines = [line for line in lines if line != '']
	stri = '\n'.join(lines)
	write_file(Get_utube_video_title_Input_File_Name, stri, mode )
	messagebox.showinfo( "Hello Python", "Data File repaired.")


"""
Nutrition Functions
"""
def add_shopping_list_to_inventory(food_name,food_quantity_digit,food_quantity_unit):
	"""
	Converting Purchasing_Unit
	kg,grams = kg,grams_to_kg
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
	
	results = mydb.select(['Food_Id','Purchasing_Unit'], f"""`Name`='{food_name}'""" ,'nutrition_values')
	Food_Id = results[0]['Food_Id']
	Purchasing_Unit = results[0]['Purchasing_Unit']

	results = mydb.select(['Food_Id','quantity','unit'],f"""`Food_Id` = '{Food_Id}'""","food_inventory")
	if results == ():
		mydb.insert(['Food_Id','food_name','quantity','unit'],[Food_Id,food_name,food_quantity_digit,food_quantity_unit],'food_inventory')
	else:
		#add the quantity
		row = results[0]
		quantity = float(row['quantity'])

		if row['unit'] == food_quantity_unit:
			quantity = food_quantity_digit + quantity
			quantity = str(quantity)
			mydb.edit(['quantity'],[quantity],f"""`Food_Id` = '{Food_Id}'""","food_inventory")



def New_Exercise_Entry_Form():
	New_Exercise_Form = tkinter.Toplevel(top_frame)
	New_Exercise_Form.geometry("400x400")
	New_Exercise_Name_Label = tkinter.Label(New_Exercise_Form, text="Exercise Name")
	New_Exercise_Name_Label.pack()
	New_Exercise_Name_Entry = tkinter.Entry(New_Exercise_Form)
	New_Exercise_Name_Entry.pack(padx=5)
	New_Exercise_Target_Label = tkinter.Label(New_Exercise_Form, text="Target Bodypart")
	New_Exercise_Target_Label.pack()
	#query = "Select * From `human_anatomy`"
	result = mydb.select('*',"","human_anatomy")
	list_ = [line['body_part_name'] + " - " + line['part_synonyms'] for line in result]
	New_Exercise_Target_Entry = AutocompleteEntry(list_, New_Exercise_Form, bd = 2, width=30)
	New_Exercise_Target_Entry.pack(padx=5)
	## Solution for multiple target:
	## Place A ListBox and Button("Add to Target List") to show Entered multiple Target Muscle
	## Each Time user type a word or select from suggestion in Entry and press Button("Add to Target List"), Entry will be cleared and the previous word will be added into listbox.
	## This process will be repeated for every muscle group user want to enter
	## All the entered muscle group will be in ListBox, take all the muscle group name from listbox and add them with ',' into a string. This will be the final target of that exercise.
	New_Exercise_Type_Label = tkinter.Label(New_Exercise_Form, text="Type-")
	New_Exercise_Type_Label.pack()
	New_Exercise_Type_Entry = AutocompleteEntry(['isolation','compound','freehand','cardio'], New_Exercise_Form, bd = 2, width=15)
	New_Exercise_Type_Entry.pack(padx=5)
	New_Exercise_Instrument_Label = tkinter.Label(New_Exercise_Form, text="Instrument-")
	New_Exercise_Instrument_Label.pack()
	#query = "Select * From `exercise_instruments`"
	result = mydb.select("*","","exercise_instruments")
	New_Exercise_Instrument_Entry = AutocompleteEntry([line['name'] for line in result], New_Exercise_Form, bd = 2, width=15)
	New_Exercise_Instrument_Entry.pack(padx=5)
	New_Exercise_Comment_Label = tkinter.Label(New_Exercise_Form, text="Comment")
	New_Exercise_Comment_Label.pack()
	New_Exercise_Comment_Entry = tkinter.Entry(New_Exercise_Form)
	New_Exercise_Comment_Entry.pack(padx=5)

	def ok():
		Name = New_Exercise_Name_Entry.get()
		Target = New_Exercise_Target_Entry.get()
		if '-' in Target: Target = Target.split('-')[1].strip()
		Type = New_Exercise_Type_Entry.get()
		Instrument = New_Exercise_Instrument_Entry.get()
		#Intrument Suggestions is shown from exercise_intruments database
		#query = "SELECT * FROM `exercise_instruments` WHERE `name` = '"+Instrument+"'"
		result = mydb.select("*","`name` = '"+Instrument+"'","exercise_instruments")
		#if This instrument is not available in exercise_instruments database, then add it their also.
		if result == ():
			#query = "INSERT INTO `exercise_instruments` (`name`) VALUES ('"+Instrument+"')"
			result = mydb.insert(['name'],[Instrument],"exercise_instruments")
		
		Comment = New_Exercise_Comment_Entry.get()
		Comment = Comment.replace("'","\\'")
		Comment = Comment.replace("\"","\\\"")
		
		#query = "INSERT INTO `exercise_data` (`name`,`target`,`type`,`instrument`,`comment`) VALUES ('"+Name+"','"+Target+"','"+Type+"','"+Instrument+"','"+Comment+"')"
		mydb.insert(['name','target','type','instrument','comment'],[Name,Target,Type,Instrument,Comment],"exercise_data")
		
		New_Exercise_Form.destroy()

	New_Exercise_Submit_Button = tkinter.Button(New_Exercise_Form, text="Submit", command=ok)
	New_Exercise_Submit_Button.pack()



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

#query = "SELECT `value` FROM `constants` where `name` = 'Resource_Categories'"
search_result = mydb.select(['value'],"`name` = 'Resource_Categories'","constants")
OPTIONS = [line['value'] for line in search_result][0].split(',')
OPTIONS.append('NEW')

top_frame = tkinter.Tk()
top_frame.tk.call('encoding', 'system', 'utf-8')
top_frame.title("Project-Super-Human")
top_frame.geometry("1000x800")




content_frame = tkinter.Frame(top_frame, bg = 'red', relief=tkinter.RAISED, borderwidth=1)
content_frame.grid(row = 0, column = 1, pady=10)

Life_Frame = tkinter.Frame(top_frame, bg = 'indigo', relief=tkinter.RAISED, borderwidth=1)
Life_Frame.grid(sticky = 'W', row = 1, column = 1)

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


Label_Frame_1 = tkinter.Label(content_frame, text = "Content Section")
L1 = tkinter.Label(content_frame, text = "Resource Url")
L2 = tkinter.Label(content_frame, text = "Category")
E1 = tkinter.Entry(content_frame, bd = 5,width=30)
D1_category = tkinter.StringVar(content_frame)
D1_category.set(OPTIONS[0]) # default value

def select_category_action(*args):
	option1 = D1_category.get()
	if option1 == 'NEW':
		d = MyDialog(top_frame)
		top_frame.wait_window(d.top)
		new_category = d.value
		add_category(new_category)
		menu = D1['menu']
		menu.delete(0, 'end')


		OPTIONS[-1] = new_category
		OPTIONS.append('NEW')
		for c in OPTIONS:
			menu.add_command(label=c)
			D1_category.set(new_category)
		
		


	

D1 = tkinter.OptionMenu(content_frame, D1_category, *OPTIONS, command = select_category_action)
B1 = tkinter.Button(content_frame,text="Enter Url",command = take_new_url)


Label_Frame_1.grid(row=1, column=1)
L1.grid(row=2, column=1)
E1.grid(row=2, column=2)
B1.grid(row=3, column=2)
L2.grid(row=2, column=3)
D1.grid(row=2, column=4)



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


def sleep_add_form():
	"""initialize database """
	if mydb.execute("SELECT * FROM sleep_data") == ():
		query_ = "INSERT INTO `sleep_data` (`id`,`bed_time`, `wakeup_time`, `todays_slept_time`, `todays_deficit_or_excess_sleep_time`, `overall_sleep_excess_or_deficit_time`, `min_required_sleep_time`) VALUES (1,'', '', '', '0hours', '0hours', '0hours')"
		result = mydb.execute(query_)

	"""initialize database """

	query = "SELECT * FROM sleep_data WHERE `id` != 1 ORDER BY id DESC LIMIT 1"
	last_result = mydb.execute(query)
	
	if last_result != ():
		last_result = last_result[0]

	if last_result == ():
		min_req_time = '8hours'
		overall_sleep_excess_or_deficit_time = '0hours'
		bed_time = "date/month/year <hour>:<min>AM"
		wakeup_time = "date/month/year <hour>:<min>AM"
	elif last_result['todays_slept_time'] != '0000-00-00 00:00:00':		
		min_req_time = str(last_result['min_required_sleep_time'])
		overall_sleep_excess_or_deficit_time = last_result['overall_sleep_excess_or_deficit_time']
		if overall_sleep_excess_or_deficit_time == '': overall_sleep_excess_or_deficit_time = '0hours'
		bed_time = "date/month/year <hour>:<min>AM"
		wakeup_time = "date/month/year <hour>:<min>AM"
	else:
		min_req_time = str(last_result['min_required_sleep_time'])
		overall_sleep_excess_or_deficit_time = last_result['overall_sleep_excess_or_deficit_time']
		if overall_sleep_excess_or_deficit_time == '': overall_sleep_excess_or_deficit_time = '0hours'
		
		if last_result['bed_time'] != '0000-00-00 00:00:00':
			bed_time = last_result['bed_time'].strftime("%d/%m/%y %I:%M%p")
			wakeup_time = "date/month/year <hour>:<min>AM"
		elif last_result['wakeup_time'] != '0000-00-00 00:00:00':
			wakeup_time = last_result['wakeup_time'].strftime("%d/%m/%y %I:%M%p")
			bed_time = "date/month/year <hour>:<min>AM"

		

	Current_Date_Bed_Var = tkinter.StringVar(content_frame)
	Current_Date_Bed_Var.set(bed_time)
	Current_Date_Awake_Var = tkinter.StringVar(content_frame)
	Current_Date_Awake_Var.set(wakeup_time)
	Sleep_Required_Minimum_Var = tkinter.StringVar(content_frame)
	Sleep_Required_Minimum_Var.set(min_req_time)
	Sleep_Deficit_Var = tkinter.StringVar(content_frame)
	Sleep_Deficit_Var.set("Overall Sleep Deficit = "+overall_sleep_excess_or_deficit_time)

	def sleep_form_submit():
		query = "SELECT * FROM sleep_data WHERE `id` != 1 ORDER BY id DESC LIMIT 1"
		last_result = mydb.execute(query)

		if last_result != ():
			last_result = last_result[0]
			overall_sleep_excess_or_deficit_time = last_result['overall_sleep_excess_or_deficit_time']
			if overall_sleep_excess_or_deficit_time == '': overall_sleep_excess_or_deficit_time = '0hours'
			overall_sleep_excess_or_deficit_time = str2deltatime(overall_sleep_excess_or_deficit_time)
		else:
			overall_sleep_excess_or_deficit_time = '0hours'
			overall_sleep_excess_or_deficit_time = str2deltatime(overall_sleep_excess_or_deficit_time)


		bedtime = Sleep_Start_Entry.get()
		gateuptime = Sleep_Gateup_Entry.get()
		reqtime_ = Sleep_Required_Minimum_Entry.get()
		reqtime = str2deltatime(reqtime_)
				

		if last_result == ():
			if bedtime != 'date/month/year <hour>:<min>AM' and gateuptime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				slept_time_delta = gateuptime_obj - bedtime_obj
				deficit_seconds = (slept_time_delta - reqtime).total_seconds()
				overall_sleep_excess_or_deficit_time = overall_sleep_excess_or_deficit_time + (slept_time_delta - reqtime)
				overall_sleep_excess_or_deficit_time_seconds = overall_sleep_excess_or_deficit_time.total_seconds()
				overall_simplified_deficit_time = simplify_time(str(overall_sleep_excess_or_deficit_time_seconds)+"seconds")
				simplified_deficit_time = simplify_time(str(deficit_seconds)+"seconds")
				bedtime = str(bedtime_obj)
				gateuptime = str(gateuptime_obj)
				slept_time = str(slept_time_delta)

				mydb.insert(['bed_time','wakeup_time','todays_slept_time','min_required_sleep_time','todays_deficit_or_excess_sleep_time','overall_sleep_excess_or_deficit_time'],[bedtime,gateuptime,slept_time, reqtime_, simplified_deficit_time, overall_simplified_deficit_time],"sleep_data")

			elif bedtime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				bedtime = str(bedtime_obj)
				mydb.insert(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"sleep_data")
			elif gateuptime != 'date/month/year <hour>:<min>AM':
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				gateuptime = str(gateuptime_obj)
				mydb.insert(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"sleep_data")


		elif last_result['todays_slept_time'] != '0000-00-00 00:00:00':
			if bedtime != 'date/month/year <hour>:<min>AM' and gateuptime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				slept_time_delta = gateuptime_obj - bedtime_obj
				deficit_seconds = (slept_time_delta - reqtime).total_seconds()
				overall_sleep_excess_or_deficit_time = overall_sleep_excess_or_deficit_time + (slept_time_delta - reqtime)
				overall_sleep_excess_or_deficit_time_seconds = overall_sleep_excess_or_deficit_time.total_seconds()
				overall_simplified_deficit_time = simplify_time(str(overall_sleep_excess_or_deficit_time_seconds)+"seconds")
				simplified_deficit_time = simplify_time(str(deficit_seconds)+"seconds")
				bedtime = str(bedtime_obj)
				gateuptime = str(gateuptime_obj)
				slept_time = str(slept_time_delta)

				mydb.insert(['bed_time','wakeup_time','todays_slept_time','min_required_sleep_time','todays_deficit_or_excess_sleep_time','overall_sleep_excess_or_deficit_time'],[bedtime,gateuptime,slept_time, reqtime_, simplified_deficit_time, overall_simplified_deficit_time],"sleep_data")
				#if last_result['bed_time'] != '0000-00-00 00:00:00':

			elif bedtime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				bedtime = str(bedtime_obj)
				mydb.insert(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"sleep_data")
			elif gateuptime != 'date/month/year <hour>:<min>AM':
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				gateuptime = str(gateuptime_obj)
				mydb.insert(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"sleep_data")

		else:
			if bedtime != 'date/month/year <hour>:<min>AM' and gateuptime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				slept_time_delta = gateuptime_obj - bedtime_obj
				deficit_seconds = (slept_time_delta - reqtime).total_seconds()
				overall_sleep_excess_or_deficit_time = overall_sleep_excess_or_deficit_time + (slept_time_delta - reqtime)
				overall_sleep_excess_or_deficit_time_seconds = overall_sleep_excess_or_deficit_time.total_seconds()
				overall_simplified_deficit_time = simplify_time(str(overall_sleep_excess_or_deficit_time_seconds)+"seconds")
				simplified_deficit_time = simplify_time(str(deficit_seconds)+"seconds")
				bedtime = str(bedtime_obj)
				gateuptime = str(gateuptime_obj)
				slept_time = str(slept_time_delta)
				
				mydb.edit(['bed_time','wakeup_time','todays_slept_time','min_required_sleep_time','todays_deficit_or_excess_sleep_time','overall_sleep_excess_or_deficit_time'],[bedtime,gateuptime,slept_time, reqtime_, simplified_deficit_time, overall_simplified_deficit_time],"`id` = "+str(last_result['id']),"sleep_data")

			elif bedtime != 'date/month/year <hour>:<min>AM':
				bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
				bedtime = str(bedtime_obj)
				mydb.edit(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"`id` = "+str(last_result['id']),"sleep_data")
			elif gateuptime != 'date/month/year <hour>:<min>AM':
				gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
				gateuptime = str(gateuptime_obj)
				mydb.edit(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"`id` = "+str(last_result['id']),"sleep_data")


		Sleep_Registry_Form.destroy()
	

	Sleep_Registry_Form = tkinter.Toplevel(top_frame)
	Sleep_Registry_Form.geometry("400x400")
	Sleep_Registry_Form_Label = tkinter.Label(Sleep_Registry_Form, text = "Sleep Section")
	Sleep_Start_Label = tkinter.Label(Sleep_Registry_Form, text = "Bed Time-")
	Sleep_Start_Entry = tkinter.Entry(Sleep_Registry_Form, bd = 2,width=32, textvariable=Current_Date_Bed_Var)
	Sleep_Gateup_Label = tkinter.Label(Sleep_Registry_Form, text = "Gateup Time-")
	Sleep_Gateup_Entry = tkinter.Entry(Sleep_Registry_Form, bd = 2,width=32, textvariable=Current_Date_Awake_Var)
	Sleep_Required_Minimum_Label = tkinter.Label(Sleep_Registry_Form, text = "Min. Required Time-")
	Sleep_Required_Minimum_Entry = tkinter.Entry(Sleep_Registry_Form, bd = 2,width=32, textvariable=Sleep_Required_Minimum_Var)
	Sleep_Deficit_Label = tkinter.Label(Sleep_Registry_Form, textvariable = Sleep_Deficit_Var)
	Sleep_Submit_Button = tkinter.Button(Sleep_Registry_Form, text="Submit", command=sleep_form_submit)
	Recovery_or_Less_Time_Label = tkinter.Label(Sleep_Registry_Form, text = "Extra Recovery Sleep Time Allowed-")
	Recovery_or_Less_Time_Entry = tkinter.Entry(Sleep_Registry_Form, bd = 2,width=15)


	Sleep_Start_Label.grid(sticky="W", row=2 , column=1 )
	Sleep_Start_Entry.grid(sticky="W", row=2 , column=2 )
	Sleep_Gateup_Label.grid(sticky="W", row=3 , column=1 )
	Sleep_Gateup_Entry.grid(sticky="W", row=3 , column=2 )
	Sleep_Required_Minimum_Label.grid(sticky="W", row=4 , column=1 )
	Sleep_Required_Minimum_Entry.grid(sticky="W", row=4 , column=2 )
	Sleep_Deficit_Label.grid(sticky="W", row=5 , column=1 )
	Recovery_or_Less_Time_Label.grid(sticky="W", row=6 , column=1 )
	Recovery_or_Less_Time_Entry.grid(sticky="W", row=6 , column=2 )
	
	Sleep_Submit_Button.grid(sticky="W", row=7 , column=2 )


Sleep_Section_Frame = tkinter.Frame(Life_Frame, bg = 'red', relief=tkinter.RAISED, borderwidth=1)
Sleep_Section_Frame_Label = tkinter.Label(Sleep_Section_Frame, text = "Sleep Section-")
Sleep_Section_Button = tkinter.Button(Sleep_Section_Frame, text="Open", command=sleep_add_form)


Exercise_Section_Frame = tkinter.Frame(Life_Frame, bg = 'green', relief=tkinter.RAISED, borderwidth=1)
Exercise_Section_Frame_Label = tkinter.Label(Exercise_Section_Frame, text = "Exercise Section")

def Record_Todays_Exercise_Form():
	Todays_Exercise_Record_Form = tkinter.Toplevel(top_frame)
	Todays_Exercise_Record_Form.geometry("400x400")

	Exercise_Date_Label = tkinter.Label(Todays_Exercise_Record_Form, text="Date")
	Exercise_Date_Label.pack()

	Exercise_Date_entryText = StringVar()
	Exercise_Date_Entry = tkinter.Entry(Todays_Exercise_Record_Form,textvariable=Exercise_Date_entryText)
	Exercise_Date_Entry.pack()
	Exercise_Date_entryText.set(datetime)

	Exercise_Name_Label = tkinter.Label(Todays_Exercise_Record_Form, text="Exercise Name")
	Exercise_Name_Label.pack()	
	
	#query = "Select * From `exercise_data`"
	result = mydb.select("*","","exercise_data")

	list_ = [line['name'] for line in result]
	Exercise_Name_entryText = StringVar()
	Exercise_Name_Entry =  AutocompleteEntry(list_, Todays_Exercise_Record_Form, bd = 2, width=30)
	Exercise_Name_Entry.pack(padx=5)
	

	Exercise_Sets_Label = tkinter.Label(Todays_Exercise_Record_Form, text="Sets")
	Exercise_Sets_Label.pack()
	Exercise_Sets_entryText = StringVar()
	Exercise_Sets_Entry = tkinter.Entry(Todays_Exercise_Record_Form,textvariable=Exercise_Sets_entryText)
	Exercise_Sets_Entry.pack()
	Exercise_Reps_Label = tkinter.Label(Todays_Exercise_Record_Form, text="Reps")
	Exercise_Reps_Label.pack()
	Exercise_Reps_entryText = StringVar()
	Exercise_Reps_Entry = tkinter.Entry(Todays_Exercise_Record_Form, textvariable=Exercise_Reps_entryText)
	Exercise_Reps_Entry.pack()
	Exercise_Quantity_Label = tkinter.Label(Todays_Exercise_Record_Form, text="Quantity")
	Exercise_Quantity_Label.pack()
	Exercise_Quantity_entryText = StringVar()
	Exercise_Quantity_Entry = tkinter.Entry(Todays_Exercise_Record_Form, textvariable=Exercise_Quantity_entryText)
	Exercise_Quantity_Entry.pack()

	#query = "Select `value` From `constants` where `name` = 'Exercise_Quantity_Units'"
	result = mydb.select(['value'],"`name` = 'Exercise_Quantity_Units'","constants")

	OPTIONS = [line['value'] for line in result][0].split(',')
	Exercise_Units_var = tkinter.StringVar(Todays_Exercise_Record_Form)
	Exercise_Units_var.set(OPTIONS[0]) # default value
	Exercise_Quantity_Units_D = tkinter.OptionMenu(Todays_Exercise_Record_Form, Exercise_Units_var, *OPTIONS, command = select_category_action)
	Exercise_Quantity_Units_D.pack()		

	def ok(destroy = True):
		Date = Exercise_Date_Entry.get()
		Name = Exercise_Name_Entry.get()
		#if exercise is not in the exercise_data then appear a dialog box if user want to add this in database. If press ok, then get Add new exercise form (Pass the exercise name)
		#Do the same for instrument while adding New exercise
		Sets = Exercise_Sets_Entry.get()
		Reps = Exercise_Reps_Entry.get()
		Quantity = Exercise_Quantity_Entry.get()
		Unit = Exercise_Units_var.get()
		#query = "INSERT INTO `daily_exercise_record` (`exercise_date`,`exercise_name`,`exercise_quantity`,`exercise_quantity_unit`,`exercise_sets`,`exercise_reps`) VALUES ('"+Date+"','"+Name+"','"+Quantity+"','"+Unit+"','"+Sets+"','"+Reps+"')"
		mydb.insert(['exercise_date','exercise_name','exercise_quantity','exercise_quantity_unit','exercise_sets','exercise_reps'],[Date,Name,Quantity,Unit,Sets,Reps],"daily_exercise_record")
		if(destroy): Todays_Exercise_Record_Form.destroy()
		else:
			Exercise_Name_entryText.set('')
			Exercise_Quantity_entryText.set('')
			Exercise_Sets_entryText.set('')
			Exercise_Reps_entryText.set('')

	def ok_a():
		ok(False)

	New_Exercise_Submit_Button = tkinter.Button(Todays_Exercise_Record_Form, text="Submit", command=ok)
	New_Exercise_Submit_Button.pack()

	New_Exercise_Submit_And_Add_Another_Button = tkinter.Button(Todays_Exercise_Record_Form, text="Submit And Add Another", command=ok_a)
	New_Exercise_Submit_And_Add_Another_Button.pack()


def This_Week_Exercise_Form():
	def add_exercises_to_weekly_plan():
		import datetime
		Day_Exercises = Day_Exercises_Planning_Exercises_Entry.get()
		Day_Choice = week_opvar.get()
		results = mydb.select(['workout_id'],"`name`='"+Day_Exercises+"'","workout_moves_data")
		result = results[0]
		exercise_id = result['workout_id']

		#todays_day = datetime.datetime.now()
		#todays_day = todays_day.strftime("%a")
		
		results = mydb.select(['day_exercises_ids'],"`day`='"+Day_Choice+"'","day_exercise_planning")
		if results == ():
			mydb.insert(['day','day_exercises_ids'],[Day_Choice,exercise_id],'day_exercise_planning')
		else:
			result = results[0]
			day_exercises = result['day_exercises_ids']
			day_exercises_li = day_exercises.split(',')
			if exercise_id in day_exercises_li:
				pass
			else:
				day_exercises = day_exercises + "," + exercise_id
				mydb.edit(['day_exercises_ids'],[day_exercises],"`day` = '"+Day_Choice+"'","day_exercise_planning")


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




	
Todays_Exercise_Record_Button = tkinter.Button(Exercise_Section_Frame, text="Record Todays Exercise", command = Record_Todays_Exercise_Form)
Exercise_Add_New_Exercise_Button = tkinter.Button(Exercise_Section_Frame, text="Add New Exercise", command = New_Exercise_Entry_Form)
Plan_This_Week_Exercise_Button = tkinter.Button(Exercise_Section_Frame, text="Plan This Week", command = This_Week_Exercise_Form)


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




Nutrition_Section_Frame = tkinter.Frame(Life_Frame, bg = 'blue', relief=tkinter.RAISED, borderwidth=1)
Nutrition_Section_Frame_Label = tkinter.Label(Nutrition_Section_Frame, text = "Nutrition Section")
Nutrition_Section_Open_Button = tkinter.Button(Nutrition_Section_Frame, text = "Open", command=nutrition_form)



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


Grooming_Section_Frame = tkinter.Frame(Life_Frame, bg = 'violet', relief=tkinter.RAISED, borderwidth=1)
Grooming_Section_Frame_Label = tkinter.Label(Grooming_Section_Frame, text = "Grooming Section")



Goal_Section_Frame = tkinter.Frame(top_frame, bg = 'orange', relief=tkinter.RAISED, borderwidth=1)
Goal_Section_Frame_Label = tkinter.Label(Goal_Section_Frame, text = "Goal Section")

Day_Planning_Section_Frame = tkinter.Frame(top_frame, bg = 'blue', relief=tkinter.RAISED, borderwidth=1)
Day_Planning_Section_Frame_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Day Planning Section")
Day_Planning_Section_Frame_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Important")
Day_Planning_Section_Frame_Not_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Not Important")
Day_Planning_Section_Frame_Now_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Now")
Day_Planning_Section_Frame_Later_Important_Label = tkinter.Label(Day_Planning_Section_Frame, text = "Later")
Day_Planning_Section_First_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
Day_Planning_Section_Second_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
Day_Planning_Section_Third_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')
Day_Planning_Section_Fourth_Grid = tkscrolled.ScrolledText(Day_Planning_Section_Frame, width=20, height=10, wrap='word')



#TKScrollTXT.insert(1.0, 'sdsi')



Social_Section_Frame = tkinter.Frame(top_frame, bg = 'green', relief=tkinter.RAISED, borderwidth=1)
Social_Section_Frame_Label = tkinter.Label(Social_Section_Frame, text = "Social Section")


Goal_Section_Frame.grid(sticky="w",row=0,column=2)
Goal_Section_Frame_Label.grid(sticky="w",row=1,column=1)

Day_Planning_Section_Frame.grid(sticky="w",row=1,column=2)
Day_Planning_Section_Frame_Label.grid(sticky="w",row=1,column=1)

Day_Planning_Section_First_Grid.grid(sticky="w",row=3,column=2)
Day_Planning_Section_Second_Grid.grid(sticky="w",row=3,column=3)
Day_Planning_Section_Third_Grid.grid(sticky="w",row=4,column=2)
Day_Planning_Section_Fourth_Grid.grid(sticky="w",row=4,column=3)

Day_Planning_Section_Frame_Important_Label.grid(sticky="w",row=3,column=1)
Day_Planning_Section_Frame_Not_Important_Label.grid(sticky="w",row=4,column=1)
Day_Planning_Section_Frame_Now_Important_Label.grid(sticky="w",row=2,column=2)
Day_Planning_Section_Frame_Later_Important_Label.grid(sticky="w",row=2,column=3)

Social_Section_Frame.grid(sticky="w",row=2,column=2)
Social_Section_Frame_Label.grid(sticky="w",row=1,column=1)


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

Sleep_Section_Frame.grid(sticky="W", row = 1, column = 2)
Sleep_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)
Sleep_Section_Button.grid(sticky="W", row = 1, column = 2)


Exercise_Section_Frame.grid(sticky="W", row = 2, column = 1)
Exercise_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)
Todays_Exercise_Record_Button.grid(sticky="W", row = 1, column = 2, padx=5)
Exercise_Add_New_Exercise_Button.grid(sticky="W", row = 1, column = 3)
Plan_This_Week_Exercise_Button.grid(sticky="W", row = 1, column = 4)

Nutrition_Section_Frame.grid(sticky="W", row = 2, column = 2)
Nutrition_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)
Nutrition_Section_Open_Button.grid(sticky="W", row = 1, column = 2)


Grooming_Section_Frame.grid(sticky="W", row = 3, column = 2)
Grooming_Section_Frame_Label.grid(sticky="W", row = 1, column = 1)

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


top_frame.mainloop()