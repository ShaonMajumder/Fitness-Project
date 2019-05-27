#import modules
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from utilities.utility import *
from utilities.mysql_database import *
from Tkinter.Login_Register import *
from Tkinter.Tkinter_Common import *

import shutil
import os
import hashlib
import datetime

datetime_ = datetime.datetime.now().strftime("%d/%m/%y")

profile_picture_folder = 'imgs/'
utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
gmail_user = config['GMAIL']['email']
gmail_password = config['GMAIL']['password']
##database config
host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']
mydb = mysql_db(host, user, password, db, charset, cursorclass)

screen_width, screen_height = get_screen_size()
Section_Height = 250
Section_Width = 340
Section_Title_Height = 2
Section_Body_Height = Section_Height - Section_Title_Height
allowed_n_columns = int(screen_width / Section_Width)
allowed_n_rows = int(screen_height / Section_Height)
n_columns = 3
n_rows = 2



def Record_Todays_Exercise_Form(top_frame):
    Todays_Exercise_Record_Form = Toplevel(top_frame)
    Todays_Exercise_Record_Form.geometry("400x400")

    Exercise_Date_Label = Label(Todays_Exercise_Record_Form, text="Date")
    Exercise_Date_Label.pack()

    Exercise_Date_entryText = StringVar()
    Exercise_Date_Entry = Entry(Todays_Exercise_Record_Form,textvariable=Exercise_Date_entryText)
    Exercise_Date_Entry.pack()
    Exercise_Date_entryText.set(datetime_)

    Exercise_Name_Label = Label(Todays_Exercise_Record_Form, text="Exercise Name")
    Exercise_Name_Label.pack()  
    
    #query = "Select * From `exercise_data`"
    result = mydb.select("*","","exercise_data")

    list_ = [line['name'] for line in result]
    Exercise_Name_entryText = StringVar()
    Exercise_Name_Entry =  AutocompleteEntry(list_, Todays_Exercise_Record_Form, bd = 2, width=30)
    Exercise_Name_Entry.pack(padx=5)
    

    Exercise_Sets_Label = Label(Todays_Exercise_Record_Form, text="Sets")
    Exercise_Sets_Label.pack()
    Exercise_Sets_entryText = StringVar()
    Exercise_Sets_Entry = Entry(Todays_Exercise_Record_Form,textvariable=Exercise_Sets_entryText)
    Exercise_Sets_Entry.pack()
    Exercise_Reps_Label = Label(Todays_Exercise_Record_Form, text="Reps")
    Exercise_Reps_Label.pack()
    Exercise_Reps_entryText = StringVar()
    Exercise_Reps_Entry = Entry(Todays_Exercise_Record_Form, textvariable=Exercise_Reps_entryText)
    Exercise_Reps_Entry.pack()
    Exercise_Quantity_Label = Label(Todays_Exercise_Record_Form, text="Quantity")
    Exercise_Quantity_Label.pack()
    Exercise_Quantity_entryText = StringVar()
    Exercise_Quantity_Entry = Entry(Todays_Exercise_Record_Form, textvariable=Exercise_Quantity_entryText)
    Exercise_Quantity_Entry.pack()

    #query = "Select `value` From `constants` where `name` = 'Exercise_Quantity_Units'"
    result = mydb.select(['value'],"`name` = 'Exercise_Quantity_Units'","constants")

    OPTIONS = [line['value'] for line in result][0].split(',')
    Exercise_Units_var = StringVar(Todays_Exercise_Record_Form)
    Exercise_Units_var.set(OPTIONS[0]) # default value
    Exercise_Quantity_Units_D = OptionMenu(Todays_Exercise_Record_Form, Exercise_Units_var, *OPTIONS, command = select_category_action)
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

    New_Exercise_Submit_Button = Button(Todays_Exercise_Record_Form, text="Submit", command=ok)
    New_Exercise_Submit_Button.pack()

    New_Exercise_Submit_And_Add_Another_Button = Button(Todays_Exercise_Record_Form, text="Submit And Add Another", command=ok_a)
    New_Exercise_Submit_And_Add_Another_Button.pack()


def This_Week_Exercise_Form(top_frame):
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


    This_Week_Exercise_Form = Toplevel(top_frame)
    This_Week_Exercise_Form.geometry("600x400")
    This_Week_Exercise_Form.title("Plan Meal")

    ex_results = mydb.select(['name'],"","workout_moves_data")
    ex_list_ = [result['name'] for result in ex_results]
    week_opvar = StringVar()
    week_days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',  'friday']
    week_opvar.set(week_days[0])

    Day_Exercises_Planning_Day_Label =  Label(This_Week_Exercise_Form, text = "Day")
    Day_Exercises_Planning_Day_Option = OptionMenu(This_Week_Exercise_Form, week_opvar, *week_days) # command = select_category_action
    Day_Exercises_Planning_Exercises_Label = Label(This_Week_Exercise_Form, text = "Exercise")
    Day_Exercises_Planning_Exercises_Entry = AutocompleteEntry(ex_list_, This_Week_Exercise_Form, bd = 2, width=30)
    Day_Exercises_Planning_Submit_Button = Button(This_Week_Exercise_Form, text="Submit", command=add_exercises_to_weekly_plan)

    Day_Exercises_Planning_Day_Label.grid(sticky="w",row=1,column=1)
    Day_Exercises_Planning_Day_Option.grid(sticky="w",row=1,column=2)
    Day_Exercises_Planning_Exercises_Label.grid(sticky="w",row=1,column=3)
    Day_Exercises_Planning_Exercises_Entry.grid(sticky="w",row=1,column=4)
    Day_Exercises_Planning_Submit_Button.grid(sticky="w",row=2,column=1)

def New_Exercise_Entry_Form_ok():
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

def New_Exercise_Entry_Form(top_frame):
    global New_Exercise_Name_Entry
    global New_Exercise_Target_Entry
    global New_Exercise_Type_Entry
    global New_Exercise_Instrument_Entry
    global New_Exercise_Comment_Entry
    
    New_Exercise_Form = top_frame
    
    #query = "Select * From `human_anatomy`"
    result = mydb.select('*',"","human_anatomy")
    list_ = [line['body_part_name'] + " - " + line['part_synonyms'] for line in result]

    
    Label(New_Exercise_Form, text="New Exercise Entry", bg="#f3af67",anchor="w").grid(row=0,columnspan=4,sticky='nesw')
    Label(New_Exercise_Form, text="Name",width=8,bg='#f19738').grid(row=1,column=0,sticky='w')
    New_Exercise_Name_Entry = Entry(New_Exercise_Form,bg='#f6a856')
    New_Exercise_Name_Entry.grid(row=1,column=1,sticky='w')
    Label(New_Exercise_Form, text="Bodypart",width=8,bg='#f19738').grid(row=1,column=2,sticky='w')
    New_Exercise_Target_Entry = AutocompleteEntry(list_, New_Exercise_Form, bd = 2, width=30,bg='#f6a856')
    New_Exercise_Target_Entry.grid(row=1,column=3,sticky='w')
    ## Solution for multiple target:
    ## Place A ListBox and Button("Add to Target List") to show Entered multiple Target Muscle
    ## Each Time user type a word or select from suggestion in Entry and press Button("Add to Target List"), Entry will be cleared and the previous word will be added into listbox.
    ## This process will be repeated for every muscle group user want to enter
    ## All the entered muscle group will be in ListBox, take all the muscle group name from listbox and add them with ',' into a string. This will be the final target of that exercise.
    Label(New_Exercise_Form, text="Type",width=8,bg='#f19738').grid(row=2,column=0,sticky='w')
    New_Exercise_Type_Entry = AutocompleteEntry(['isolation','compound','freehand','cardio'], New_Exercise_Form, bd = 2, width=15,bg='#f6a856')
    New_Exercise_Type_Entry.grid(row=2,column=1,sticky='w')
    Label(New_Exercise_Form, text="Instrument",width=8,bg='#f19738').grid(row=2,column=2,sticky='w')
    #query = "Select * From `exercise_instruments`"
    result = mydb.select("*","","exercise_instruments")
    New_Exercise_Instrument_Entry = AutocompleteEntry([line['name'] for line in result], New_Exercise_Form, bd = 2, width=15,bg='#f6a856')
    New_Exercise_Instrument_Entry.grid(row=2,column=3,sticky='w')
    
    Label(New_Exercise_Form, text="Comment",width=8,bg='#f19738').grid(row=3,column=0,sticky='w')
    New_Exercise_Comment_Entry = Entry(New_Exercise_Form,bg='#f6a856')
    New_Exercise_Comment_Entry.grid(row=3,column=1,sticky='w')
    Frame_Submit = Frame(New_Exercise_Form)
    Frame_Submit.columnconfigure(0, weight=Section_Width)
    Frame_Submit.grid(row=4,columnspan=4,sticky='nesw')
    New_Exercise_Submit_Button = Button(Frame_Submit, text="Submit", command=New_Exercise_Entry_Form_ok, anchor='center', bg='#e38724')
    New_Exercise_Submit_Button.grid(row=0,sticky='nesw')

def draw_exercise_section_frame(top_frame):
    exercise_colors = {
        'primary_hex' : '#e49a4b',
        'header_title_hex' : '#d78b3a',
    }
    global Exercise_Section_Container_Frame
    Exercise_Section_Container_Frame = Frame(top_frame, bg = exercise_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

    @static_var("status", 'active')
    def toggle_section():
        if toggle_section.status == 'hidden':
            Exercise_Section_Active_Container_Frame.grid()
            Exercise_Section_Inactive_Container_Frame.grid_remove()
            toggle_section.status = 'active'
        elif toggle_section.status == 'active':
            Exercise_Section_Active_Container_Frame.grid_remove()
            Exercise_Section_Inactive_Container_Frame.grid()
            toggle_section.status = 'hidden'
    

    Exercise_Section_Active_Container_Frame = Frame(Exercise_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Exercise_Section_Active_Container_Frame.grid(sticky="nesw")
    #Exercise_Section_Active_Container_Frame.grid_propagate(False)
    Exercise_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Exercise_Section_Inactive_Container_Frame = Frame(Exercise_Section_Container_Frame, bg = exercise_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Exercise_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Exercise_Section_Inactive_Container_Frame.grid_propagate(False)
    Exercise_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_section()

    img = image_to_tkinter_img(profile_picture_folder + 'gym.png',(200, 200))    

    Inactive_Button = Button(Exercise_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=exercise_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img

    
    Label(Exercise_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Exercise_Section_Active_Container_Frame, text="Exercise Section \u25E4 Hide", bg=exercise_colors['header_title_hex'], height=2, font=("Calibri", 13), command=toggle_section).grid(row=0,sticky="nesw")

    Exercise_Buttons_Frame = Frame(Exercise_Section_Active_Container_Frame, bg = exercise_colors['primary_hex'], relief=RAISED)
    Exercise_Buttons_Frame.grid(row=1,sticky="nesw")
    Exercise_Sub_Action_Frame = Frame(Exercise_Section_Active_Container_Frame, bg = exercise_colors['primary_hex'], relief=RAISED)
    Exercise_Sub_Action_Frame.grid(row=2,sticky="nesw")

    img_add_bt = image_to_tkinter_img(profile_picture_folder + 'add-circular-button.png', (20, 20))
    New_Exercise_Entry_Button = Button(Exercise_Buttons_Frame, bg='#e28c2f', text="New Workout", compound='left', image = img_add_bt, command=lambda: New_Exercise_Entry_Form(Exercise_Sub_Action_Frame) )
    New_Exercise_Entry_Button.image = img_add_bt
    New_Exercise_Entry_Button.grid(row=0,column=0,sticky="nesw")

    img_record_bt = image_to_tkinter_img(profile_picture_folder + 'record-button.png', (20, 20))
    Todays_Exercise_Record_Button = Button(Exercise_Buttons_Frame, bg='#e28c2f', text="Record Todays Workout", compound='left', image = img_record_bt, command=lambda: Record_Todays_Exercise_Form(top_frame) )
    Todays_Exercise_Record_Button.image = img_record_bt
    Todays_Exercise_Record_Button.grid(row=0,column=1,sticky="nesw")

    img_record_bt = image_to_tkinter_img(profile_picture_folder + 'week-plan-button.png', (20, 20))
    Todays_Exercise_Record_Button = Button(Exercise_Buttons_Frame, bg='#e28c2f', text="Plan week", compound='left', image = img_record_bt, command=lambda: This_Week_Exercise_Form(top_frame) )
    Todays_Exercise_Record_Button.image = img_record_bt
    Todays_Exercise_Record_Button.grid(row=0,column=2,sticky="nesw")

    return Exercise_Section_Container_Frame


def exercise_module_frame(top_frame):
    return draw_exercise_section_frame(top_frame)