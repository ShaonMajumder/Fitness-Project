#import modules 
from PIL import ImageTk,Image
import PIL
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from utilities.utility import *
from utilities.mysql_database import *
from Tkinter.Login_Register import *
import os
import hashlib

Section_Height = 250
Section_Width = 350

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


def validate_picture(filename):
    filename_ = filename.split('/')[-1]
    filename_ext = filename_.split('.')[1]
    allowed_filetypes = ['JPG','PNG']
    for ft in allowed_filetypes:
        if filename_ext == ft or filename_ext == ft.lower():
            return filename_
        else:
            print("Not allowed file type.")

def select_file():
    profile_id = session_data['profile_id']
    new_propic_filename = askopenfilename()
    filename = validate_picture(new_propic_filename)
    if(filename):
        newPath = shutil.copy(new_propic_filename, 'imgs/')
        mydb.edit(['profile_picture'],[filename],"`profile_id`='"+profile_id+"'","profiles")
    else:
        print("wrong filetype")

# Designing window for registration
 
 
# Designing window for login 
 
 
def save_profile_data():
    profile_id = session_data['profile_id']
    fullname_info = fullname.get()
    gender_info = gender.get()
    age_info = age.get()
    birthdate_info = birthdate.get()
    protein_grams_per_body_pound_info = protein_grams_per_body_pound.get()
    height_info = height.get()
    bodyweight_info = bodyweight.get()
    meal_number_info = meal_number.get()
    activity_level_info = activity_level.get()

    result = mydb.select('*',"`profile_id`='"+profile_id+"'","biodata")
    if result != ():
        mydb.edit(['fullname','gender','age','birthdate','protein_grams_per_body_pound','height','bodyweight','meal_number','activity_level'],[fullname_info,gender_info,age_info,birthdate_info,protein_grams_per_body_pound_info,height_info,bodyweight_info,meal_number_info,activity_level_info],"`profile_id`='"+profile_id+"'","biodata")
    else:
        mydb.insert(['profile_id','fullname','gender','age','birthdate','protein_grams_per_body_pound','height','bodyweight','meal_number','activity_level'],[profile_id,fullname_info,gender_info,age_info,birthdate_info,protein_grams_per_body_pound_info,height_info,bodyweight_info,meal_number_info,activity_level_info],"biodata")
    

def add_profile_details():
    profile_id = session_data['profile_id']
    global fullname
    global gender
    global age
    global birthdate
    global protein_grams_per_body_pound
    global height
    global bodyweight
    global meal_number
    global activity_level

    fullname = StringVar()
    gender = StringVar()
    age = StringVar()
    birthdate = StringVar()
    protein_grams_per_body_pound = StringVar()
    height = StringVar()
    bodyweight = StringVar()
    meal_number = StringVar()
    activity_level = StringVar()

    result = mydb.select('*',"`profile_id`='"+profile_id+"'","biodata")
    if result != ():
        row = result[0]
        fullname.set(row['fullname'])
        gender.set(row['gender'])
        age.set(row['age'])
        birthdate.set(row['birthdate'])
        protein_grams_per_body_pound.set(row['protein_grams_per_body_pound'])
        height.set(row['height'])
        bodyweight.set(row['bodyweight'])
        meal_number.set(row['meal_number'])
        activity_level.set(row['activity_level'])

    global add_profile_details_screen
    add_profile_details_screen = Toplevel(application_screen)
    add_profile_details_screen.title("Add/Edit details")
    add_profile_details_screen.geometry("300x500")
    Label(add_profile_details_screen, text="Please enter details below").pack()
    Label(add_profile_details_screen, text="").pack()    

    global fullname_entry
    global gender_entry
    global age_entry
    global birthdate_entry
    global protein_grams_per_body_pound_entry
    global height_entry
    global bodyweight_entry
    global meal_number_entry
    global activity_level_entry

    Label(add_profile_details_screen, text="Fullname * ").pack()
    fullname_entry = Entry(add_profile_details_screen, textvariable=fullname)
    fullname_entry.pack()
    Label(add_profile_details_screen, text="Gender * ").pack()
    gender_entry = Entry(add_profile_details_screen, textvariable=gender)
    gender_entry.pack()
    Label(add_profile_details_screen, text="Age * ").pack()
    age_entry = Entry(add_profile_details_screen, textvariable=age)
    age_entry.pack()
    Label(add_profile_details_screen, text="Birthdate * ").pack()
    birthdate_entry = Entry(add_profile_details_screen, textvariable=birthdate)
    birthdate_entry.pack()
    Label(add_profile_details_screen, text="Protein(grams) per bodyweight(pound)").pack()
    protein_grams_per_body_pound_entry = Entry(add_profile_details_screen, textvariable=protein_grams_per_body_pound)
    protein_grams_per_body_pound_entry.pack()
    Label(add_profile_details_screen, text="Height * ").pack()
    height_entry = Entry(add_profile_details_screen, textvariable=height)
    height_entry.pack()
    Label(add_profile_details_screen, text="Bodyweight * ").pack()
    bodyweight_entry = Entry(add_profile_details_screen, textvariable=bodyweight)
    bodyweight_entry.pack()
    Label(add_profile_details_screen, text="Meal Number * ").pack()
    meal_number_entry = Entry(add_profile_details_screen, textvariable=meal_number)
    meal_number_entry.pack()
    Label(add_profile_details_screen, text="Activity Level * ").pack()
    activity_level_entry = Entry(add_profile_details_screen, textvariable=activity_level)
    activity_level_entry.pack()
    Button(add_profile_details_screen, text="Submit", command=save_profile_data).pack()

 

def user_profile_form(*args, **kwargs):
    global user_profile_screen

    ## object,iconfile
    iconfile = kwargs['icon']
    session_data = kwargs['session_data']


    if 'object' in kwargs:
        #   type(Toplevel(Tk())).__name__ == 'Toplevel'
        object_ = kwargs['object']
        user_profile_screen = Toplevel(object_)
    else:
        #  if type(object_).__name__ == 'Tk':
        user_profile_screen = Tk()
        user_profile_screen.iconbitmap(iconfile)                   

    user_profile_screen.title("User Details")
    user_profile_screen.geometry("350x250")
    user_profile_screen.columnconfigure(0, weight=350)
    

    profile_id = session_data['profile_id']
    results = mydb.execute(f"""SELECT * FROM biodata INNER JOIN profiles ON biodata.profile_id = profiles.profile_id WHERE profiles.`profile_id` = '{profile_id}'""")
    row = results[0]
    fullname = row['fullname']
    gender = row['gender']
    age = row['age']
    height = row['height']
    bodyweight = row['bodyweight']
    meal_number = row['meal_number']
    activity_level = row['activity_level']
    profile_picture = row['profile_picture']

    user_details = f"""Name: {fullname}
Gender: {gender}
Age: {age}
Height: {height}
Body Weight: {bodyweight}
Meal Number: {meal_number}
Activity Level: {activity_level}"""

    

    profile_picture_folder="imgs/"
    if profile_picture == "":
        img_file = "profile_avatar.png"
    else:
        img_file = profile_picture
    
    original = PIL.Image.open(profile_picture_folder + img_file)
    size = (90, 90)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)
    #display = Canvas(main_screen, bd=0, highlightthickness=0)
    #display.create_image(0, 0, image=img, anchor=NW, tags="IMG")
    #display.pack()
    Label(user_profile_screen,text="User Details", bg="#969ba3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    profile_information_holder = Frame(user_profile_screen, bg = '#a7abb2', relief=RAISED, borderwidth=1)
    profile_information_holder.grid(row=1,sticky="nesw")
    panel = Label(profile_information_holder, text=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    panel.image = img
    panel.grid(rowspan=5,column=0,sticky="nesw")

    fullname = StringVar()
    gender = StringVar()
    age = StringVar()
    height = StringVar()
    bodyweight = StringVar()
    meal_number = StringVar()
    activity_level = StringVar()
    
    fullname.set(row['fullname'])
    gender.set(row['gender'])
    age.set(row['age'])
    height.set(row['height'])
    bodyweight.set(row['bodyweight'])
    meal_number.set(row['meal_number'])
    activity_level.set(row['activity_level'])
    
    Label(profile_information_holder,text="Gender :", width=11, anchor="w", bg='#b5aba4').grid(row=1,column=1,sticky="w")
    Label(profile_information_holder,text="Age :", width=11, anchor="w", bg='#b5aba4').grid(row=2,column=1,sticky="w")
    Label(profile_information_holder,text="Height :", width=11, anchor="w", bg='#b5aba4').grid(row=3,column=1,sticky="w")
    Label(profile_information_holder,text="Bodyweight :", width=11, anchor="w", bg='#b5aba4').grid(row=4,column=1,sticky="w")
    Label(profile_information_holder,text="Meal Number :", width=11, anchor="w", bg='#b5aba4').grid(row=5,column=1,sticky="w")
    Label(profile_information_holder,text="Activity Level :", width=11, anchor="w", bg='#b5aba4').grid(row=6,column=1,sticky="w")

    Label(profile_information_holder,textvariable=gender, width =5, bg='#c1b3aa').grid(row=1,column=2,sticky="w")
    Label(profile_information_holder,textvariable=age, width =5, bg='#c1b3aa').grid(row=2,column=2,sticky="w")
    Label(profile_information_holder,textvariable=height, width =5, bg='#c1b3aa').grid(row=3,column=2,sticky="w")
    Label(profile_information_holder,textvariable=bodyweight, width =5, bg='#c1b3aa').grid(row=4,column=2,sticky="w")
    Label(profile_information_holder,textvariable=meal_number, width =5, bg='#c1b3aa').grid(row=5,column=2,sticky="w")
    Label(profile_information_holder,textvariable=activity_level, width =5, bg='#c1b3aa').grid(row=6,column=2,sticky="w")

    Button(user_profile_screen,text="Add/Edit details", height="2", width="30", command = add_profile_details).grid(row=2,sticky="nesw")
    Button(profile_information_holder,text="Change", command = select_file).grid(row=6,column=0,sticky="w")
    #Button(profile_information_holder,text="Change", command = lambda: select_file(new_propic_filename)).grid(row=6,column=0,sticky="w")
    
    return user_profile_screen

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


    Sleep_Section_Container_Frame.destroy()

def intialize_sleep_database():
    global Current_Date_Bed_Var
    global Current_Date_Awake_Var
    global Sleep_Required_Minimum_Var
    global Sleep_Deficit_Var
    
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
        bed_time = "D/M/Y <h>:<m>AM"
        wakeup_time = "D/M/Y <h>:<m>AM"
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

                
    Current_Date_Bed_Var = StringVar()
    Current_Date_Bed_Var.set(bed_time)
    Current_Date_Awake_Var = StringVar()
    Current_Date_Awake_Var.set(wakeup_time)
    Sleep_Required_Minimum_Var = StringVar()
    Sleep_Required_Minimum_Var.set(min_req_time)
    Sleep_Deficit_Var = StringVar()
    Sleep_Deficit_Var.set(overall_sleep_excess_or_deficit_time)

def static_var(varname, value):
        def decorate(func):
            setattr(func, varname, value)
            return func
        return decorate

def draw_sleep_section_frame():
    global Sleep_Section_Container_Frame
    
    global Current_Date_Bed_Var
    global Current_Date_Awake_Var
    global Sleep_Required_Minimum_Var
    global Sleep_Deficit_Var
    

    Sleep_Section_Container_Frame = Frame(application_screen, bg = '#accde0', relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    Sleep_Section_Container_Frame.grid(sticky="nesw", row = 0, column = 1)
    
    
    @static_var("status", 'active')
    def toggle_sleep_section():
        if toggle_sleep_section.status == 'hidden':
            Sleep_Section_Active_Container_Frame.grid()
            Sleep_Section_Inactive_Container_Frame.grid_remove()
            toggle_sleep_section.status = 'active'
        elif toggle_sleep_section.status == 'active':
            Sleep_Section_Active_Container_Frame.grid_remove()
            Sleep_Section_Inactive_Container_Frame.grid()
            toggle_sleep_section.status = 'hidden'
    

    Sleep_Section_Active_Container_Frame = Frame(Sleep_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Sleep_Section_Active_Container_Frame.grid(sticky="nesw")
    #Sleep_Section_Active_Container_Frame.grid_propagate(False)
    Sleep_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Sleep_Section_Inactive_Container_Frame = Frame(Sleep_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Sleep_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Sleep_Section_Inactive_Container_Frame.grid_propagate(False)
    Sleep_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_sleep_section()

    
    original = PIL.Image.open(profile_picture_folder + 'sleep_section2.png')
    size = (200, 200)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)

    Label(Sleep_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Sleep_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_sleep_section, height=2,bg="LightSkyBlue3",font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Sleep_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_sleep_section, height=Section_Height, anchor="center", bg="#b1d2e0", image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    sleep_info_frame = Frame(Sleep_Section_Active_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    sleep_info_frame.grid(row=1,sticky="nesw")
    bglabel = "#bbc1d6"
    Label(sleep_info_frame, text = "Bed Time-",width=15,bg=bglabel).grid(sticky="W", row=0 , column=0 )
    Label(sleep_info_frame, text = "Gateup Time-",width=15,bg=bglabel).grid(sticky="W", row=1 , column=0 )
    Label(sleep_info_frame, text = "Min. Required Time-",width=15,bg=bglabel).grid(sticky="W", row=2 , column=0 )
    Label(sleep_info_frame, text = "Overall Sleep Deficit-",width=15,bg=bglabel).grid(sticky="W", row=3 , column=0 )
    
    bglabelentry="#d9ddea"
    Sleep_Start_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=Current_Date_Bed_Var, bg=bglabelentry)
    Sleep_Start_Entry.grid(sticky="w",row=0,column=1)
    Sleep_Gateup_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=Current_Date_Awake_Var, bg=bglabelentry)
    Sleep_Gateup_Entry.grid(sticky="w",row=1,column=1)
    Sleep_Required_Minimum_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=Sleep_Required_Minimum_Var, bg=bglabelentry)
    Sleep_Required_Minimum_Entry.grid(sticky="w",row=2,column=1)
    Sleep_Deficit_Label = Label(sleep_info_frame, width=27, textvariable = Sleep_Deficit_Var, bg=bglabelentry)
    Sleep_Deficit_Label.grid(sticky="w",row=3,column=1)
        
    Button(Sleep_Section_Active_Container_Frame, text="Submit", command=sleep_form_submit,height=2,bg="#b1d2e0").grid(sticky="nesw", row=7 )
    
    Recovery_or_Less_Time_Label = Label(sleep_info_frame, text = "Extra Recovery Sleep Time Allowed-")
    Recovery_or_Less_Time_Entry = Entry(sleep_info_frame, bd = 2,width=15)
    
    return Sleep_Section_Container_Frame


def draw_exercise_section_frame():
    global Exercise_Section_Container_Frame
    Exercise_Section_Container_Frame = Frame(application_screen, bg = '#a4d343', relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    Exercise_Section_Container_Frame.grid(sticky="nesw", row = 0, column = 2)

    @static_var("status", 'active')
    def toggle_sleep_section():
        if toggle_sleep_section.status == 'hidden':
            Exercise_Section_Active_Container_Frame.grid()
            Exercise_Section_Inactive_Container_Frame.grid_remove()
            toggle_sleep_section.status = 'active'
        elif toggle_sleep_section.status == 'active':
            Exercise_Section_Active_Container_Frame.grid_remove()
            Exercise_Section_Inactive_Container_Frame.grid()
            toggle_sleep_section.status = 'hidden'
    

    Exercise_Section_Active_Container_Frame = Frame(Exercise_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Exercise_Section_Active_Container_Frame.grid(sticky="nesw")
    #Exercise_Section_Active_Container_Frame.grid_propagate(False)
    Exercise_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Exercise_Section_Inactive_Container_Frame = Frame(Exercise_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Exercise_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Exercise_Section_Inactive_Container_Frame.grid_propagate(False)
    Exercise_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_sleep_section()

    
    original = PIL.Image.open(profile_picture_folder + 'gym.png')
    size = (200, 200)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)

    Label(Exercise_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Exercise_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_sleep_section, height=2,bg="LightSkyBlue3",font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Exercise_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_sleep_section, height=Section_Height, anchor="center", bg="#a4d343", image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    return Exercise_Section_Container_Frame

def exercise_module_frame():
    return draw_exercise_section_frame()

def draw_nutrition_section_frame():
    global Nutrition_Section_Container_Frame
    Nutrition_Section_Container_Frame = Frame(application_screen, bg = '#accde0', relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    Nutrition_Section_Container_Frame.grid(sticky="nesw", row = 1, column = 2)

    @static_var("status", 'active')
    def toggle_sleep_section():
        if toggle_sleep_section.status == 'hidden':
            Nutrition_Section_Active_Container_Frame.grid()
            Nutrition_Section_Inactive_Container_Frame.grid_remove()
            toggle_sleep_section.status = 'active'
        elif toggle_sleep_section.status == 'active':
            Nutrition_Section_Active_Container_Frame.grid_remove()
            Nutrition_Section_Inactive_Container_Frame.grid()
            toggle_sleep_section.status = 'hidden'
    

    Nutrition_Section_Active_Container_Frame = Frame(Nutrition_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Nutrition_Section_Active_Container_Frame.grid(sticky="nesw")
    #Nutrition_Section_Active_Container_Frame.grid_propagate(False)
    Nutrition_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Nutrition_Section_Inactive_Container_Frame = Frame(Nutrition_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Nutrition_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Nutrition_Section_Inactive_Container_Frame.grid_propagate(False)
    Nutrition_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_sleep_section()

    
    original = PIL.Image.open(profile_picture_folder + 'nutrition.png')
    size = (200, 200)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)

    Label(Nutrition_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Nutrition_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_sleep_section, height=2,bg="LightSkyBlue3",font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Nutrition_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_sleep_section, height=Section_Height, anchor="center", bg="#b1d2e0", image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    return Nutrition_Section_Container_Frame

def draw_grooming_section_frame():
    global Grooming_Section_Container_Frame
    Grooming_Section_Container_Frame = Frame(application_screen, bg = '#accde0', relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    Grooming_Section_Container_Frame.grid(sticky="nesw", row = 1, column = 1)

    @static_var("status", 'active')
    def toggle_sleep_section():
        if toggle_sleep_section.status == 'hidden':
            Grooming_Section_Active_Container_Frame.grid()
            Grooming_Section_Inactive_Container_Frame.grid_remove()
            toggle_sleep_section.status = 'active'
        elif toggle_sleep_section.status == 'active':
            Grooming_Section_Active_Container_Frame.grid_remove()
            Grooming_Section_Inactive_Container_Frame.grid()
            toggle_sleep_section.status = 'hidden'
    

    Grooming_Section_Active_Container_Frame = Frame(Grooming_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Grooming_Section_Active_Container_Frame.grid(sticky="nesw")
    #Grooming_Section_Active_Container_Frame.grid_propagate(False)
    Grooming_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Grooming_Section_Inactive_Container_Frame = Frame(Grooming_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Grooming_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Grooming_Section_Inactive_Container_Frame.grid_propagate(False)
    Grooming_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_sleep_section()

    
    original = PIL.Image.open(profile_picture_folder + 'grooming.png')
    size = (200, 200)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)

    Label(Grooming_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Grooming_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_sleep_section, height=2,bg="LightSkyBlue3",font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Grooming_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_sleep_section, height=Section_Height, anchor="center", bg="#b1d2e0", image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    return Grooming_Section_Container_Frame

def draw_hygene_section_frame():
    global Hygene_Section_Container_Frame
    Hygene_Section_Container_Frame = Frame(application_screen, bg = '#accde0', relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    Hygene_Section_Container_Frame.grid(sticky="nesw", row = 1, column = 0)

    @static_var("status", 'active')
    def toggle_sleep_section():
        if toggle_sleep_section.status == 'hidden':
            Hygene_Section_Active_Container_Frame.grid()
            Hygene_Section_Inactive_Container_Frame.grid_remove()
            toggle_sleep_section.status = 'active'
        elif toggle_sleep_section.status == 'active':
            Hygene_Section_Active_Container_Frame.grid_remove()
            Hygene_Section_Inactive_Container_Frame.grid()
            toggle_sleep_section.status = 'hidden'
    

    Hygene_Section_Active_Container_Frame = Frame(Hygene_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Hygene_Section_Active_Container_Frame.grid(sticky="nesw")
    #Hygene_Section_Active_Container_Frame.grid_propagate(False)
    Hygene_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Hygene_Section_Inactive_Container_Frame = Frame(Hygene_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Hygene_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Hygene_Section_Inactive_Container_Frame.grid_propagate(False)
    Hygene_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_sleep_section()

    
    original = PIL.Image.open(profile_picture_folder + 'hygene.png')
    size = (200, 200)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)

    Label(Hygene_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Hygene_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_sleep_section, height=2,bg="LightSkyBlue3",font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Hygene_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_sleep_section, height=Section_Height, anchor="center", bg="#b1d2e0", image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    return Hygene_Section_Container_Frame



def hygene_module_frame():
    return draw_hygene_section_frame()

def grooming_module_frame():
    return draw_grooming_section_frame()

def nutrition_module_frame():
    return draw_nutrition_section_frame()

def sleep_module_frame():
    intialize_sleep_database()
    return draw_sleep_section_frame()

def profile_information_section_frame():
    global session_data
    profile_id = session_data['profile_id']
    results = mydb.execute(f"""SELECT * FROM biodata INNER JOIN profiles ON biodata.profile_id = profiles.profile_id WHERE profiles.`profile_id` = '{profile_id}'""")
    row = results[0]
    profile_picture = row['profile_picture']

    profile_picture_folder="imgs/"
    if profile_picture == "":
        img_file = "profile_avatar.png"
    else:
        img_file = profile_picture
    
    original = PIL.Image.open(profile_picture_folder + img_file)
    size = (90, 90)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)
    #display = Canvas(main_screen, bd=0, highlightthickness=0)
    #display.create_image(0, 0, image=img, anchor=NW, tags="IMG")
    #display.pack()    

    fullname = StringVar()
    gender = StringVar()
    age = StringVar()
    height = StringVar()
    bodyweight = StringVar()
    meal_number = StringVar()
    activity_level = StringVar()
    
    fullname.set(row['fullname'])
    gender.set(row['gender'])
    age.set(row['age'])
    height.set(row['height'])
    bodyweight.set(row['bodyweight'])
    meal_number.set(row['meal_number'])
    activity_level.set(row['activity_level'])
    
    def draw_profile_information_section_frame():
        profile_information_frame = Frame(application_screen, bg = '#969ba3', relief=RAISED, borderwidth=1, height=Section_Height, width=Section_Width)
        profile_information_frame.grid(sticky="nesw", row=0, column=0)

        Label(profile_information_frame,text="User Details", bg="#969ba3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
        profile_information_holder = Frame(profile_information_frame, bg = '#a7abb2', relief=RAISED, borderwidth=1)
        profile_information_holder.grid(row=1,sticky="nesw")
        
        image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
        image_panel.image = img
        image_panel.grid(rowspan=5,column=0,sticky="nesw")

        Label(profile_information_holder,text="Gender :", width=11, anchor="w", bg='#b5aba4').grid(row=1,column=1,sticky="w")
        Label(profile_information_holder,text="Age :", width=11, anchor="w", bg='#b5aba4').grid(row=2,column=1,sticky="w")
        Label(profile_information_holder,text="Height :", width=11, anchor="w", bg='#b5aba4').grid(row=3,column=1,sticky="w")
        Label(profile_information_holder,text="Bodyweight :", width=11, anchor="w", bg='#b5aba4').grid(row=4,column=1,sticky="w")
        Label(profile_information_holder,text="Meal Number :", width=11, anchor="w", bg='#b5aba4').grid(row=5,column=1,sticky="w")
        Label(profile_information_holder,text="Activity Level :", width=11, anchor="w", bg='#b5aba4').grid(row=6,column=1,sticky="w")

        Label(profile_information_holder,textvariable=gender, width =5, bg='#c1b3aa').grid(row=1,column=2,sticky="w")
        Label(profile_information_holder,textvariable=age, width =5, bg='#c1b3aa').grid(row=2,column=2,sticky="w")
        Label(profile_information_holder,textvariable=height, width =5, bg='#c1b3aa').grid(row=3,column=2,sticky="w")
        Label(profile_information_holder,textvariable=bodyweight, width =5, bg='#c1b3aa').grid(row=4,column=2,sticky="w")
        Label(profile_information_holder,textvariable=meal_number, width =5, bg='#c1b3aa').grid(row=5,column=2,sticky="w")
        Label(profile_information_holder,textvariable=activity_level, width =5, bg='#c1b3aa').grid(row=6,column=2,sticky="w")
        Button(profile_information_holder,text="Change", bg="#b1b5b2", command = select_file).grid(row=6,column=0,sticky="w")
        #Button(profile_information_holder,text="Change", command = lambda: select_file(new_propic_filename)).grid(row=6,column=0,sticky="w")
        
        Button(profile_information_frame,text="Add/Edit details", height="2", width="30", bg="#b1b5b2", command = add_profile_details).grid(row=2,sticky="nesw")
        return profile_information_frame

    frame = draw_profile_information_section_frame()
    return frame

def application_form(*args, **kwargs):
    global application_screen
    global session_data
    session_data = kwargs['session_data']
    profile_id = session_data['profile_id']
    iconfile = kwargs['icon']

    if 'object' in kwargs:
        #   type(Toplevel(Tk())).__name__ == 'Toplevel'
        object_ = kwargs['object']
        application_screen = Toplevel(object_)
    else:
        #  if type(object_).__name__ == 'Tk':
        application_screen = Tk()
        application_screen.iconbitmap(iconfile)                   

    application_screen.title("Project - Super-Human")
    application_screen.geometry("1050x500")

    #application_screen.columnconfigure(0, weight=Section_Width)
    #application_screen.columnconfigure(1, weight=Section_Width)

    profile_information_frame = profile_information_section_frame()
    sleep_section_frame = sleep_module_frame()
    exercise_section_frame = exercise_module_frame()
    nutrition_section_frame = nutrition_module_frame()
    grooming_section_frame = grooming_module_frame()
    hygene_section_frame = hygene_module_frame()

    profile_information_frame.grid_propagate(False)
    profile_information_frame.columnconfigure(0, weight=Section_Width)
    sleep_section_frame.grid_propagate(False)
    sleep_section_frame.columnconfigure(0, weight=Section_Width)
    exercise_section_frame.grid_propagate(False)
    exercise_section_frame.columnconfigure(0, weight=Section_Width)
    nutrition_section_frame.grid_propagate(False)
    nutrition_section_frame.columnconfigure(0, weight=Section_Width)
    grooming_section_frame.grid_propagate(False)
    grooming_section_frame.columnconfigure(0, weight=Section_Width)
    hygene_section_frame.grid_propagate(False)
    hygene_section_frame.columnconfigure(0, weight=Section_Width)

    return application_screen

def main_account_screen():
    """
    global main_screen
    object_ = Login_Register(icon="imgs/robist_apps.ico",success_function=lambda: user_profile_form())
    main_screen = object_.frame
    def on_closing():
        exit()
    main_screen.protocol("WM_DELETE_WINDOW", on_closing)
    main_screen.mainloop()

    while object_.is_login() == False:
        pass
    """

    #object_.session_data
    application_form1 = application_form( session_data={'profile_id':'vwjjn6ip'}, icon="imgs/robist_apps.ico" )
    application_form1.mainloop()
    
main_account_screen()

"""
Flow list
1. Activate email and verify
"""