#import modules 
from PIL import ImageTk,Image
import PIL
from tkinter import *
from utilities.utility import *
from utilities.mysql_database import *
import os
import hashlib

"""
Foreign key data
SELECT username
FROM biodata
INNER JOIN profiles
ON biodata.profile_id = profiles.profile_id;
"""
global login_state
login_state = False
global session_data
session_data = {}

def set_session(profile_id):
    login_state = True
    session_data['profile_id'] = profile_id

def destroy_session():
    login_state = False
    session_data = {}

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

# Designing window for registration
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global email
    global username_entry
    global password_entry
    global email_entry
    username = StringVar()
    password = StringVar()
    email = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    email_lable = Label(register_screen, text="Email * ")
    email_lable.pack()
    email_entry = Entry(register_screen, textvariable=email)
    email_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global email_verify
    global password_verify
 
    email_verify = StringVar()
    password_verify = StringVar()
 
    global email_login_entry
    global password_login_entry
 
    Label(login_screen, text="Email * ").pack()
    email_login_entry = Entry(login_screen, textvariable=email_verify)
    email_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
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
    add_profile_details_screen = Toplevel(main_screen)
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

# Implementing event on register button
 
def register_user(): 
    username_info = username.get()
    email_info = email.get()
    password_info = password.get()
    password_result = hashlib.md5(password_info.encode())
    password_info = password_result.hexdigest()
    
    #validation required
    result_email = mydb.select('*',"`email` = '"+email_info+"'",'profiles')
    result_username = mydb.select('*',"`username` = '"+username_info+"'",'profiles')
    if(result_email == () and result_username == ()):
        while(True):
            random_key = randomString(stringLength=8)
            result = mydb.select("*",f"""`profile_id` = '{random_key}'""","profiles")
            if result != ():
                pass
            else:
                break

        mydb.insert(['profile_id','username','email','password'],[random_key,username_info,email_info,password_info],'profiles')
        sent_from = gmail_user  
        to = [email_info]
        subject = 'Activate Account - ROBIST'
        body = f"""Hey {username_info}, thanks for register with Robist account. To activate your account, click here or visit this link - .\n\n- Robist Automated Reply"""
        CC = ''
        send_email(subject, body, CC, to, sent_from, gmail_user, gmail_password)

    elif(result_email != ()):
        print("This email is already registered.")
    elif(result_username != ()):
        print("Username already taken.")
    

    username_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
 
# Implementing event on login button 
 
def login_verify():
    email1 = email_verify.get()
    password1 = password_verify.get()
    password_result = hashlib.md5(password1.encode())
    password1 = password_result.hexdigest()

    email_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    username_result = mydb.select('*',f"""`email`='{email1}'""","profiles")
    if username_result != ():
        password_result = mydb.select('*',f"""`password`='{password1}'""","profiles")
        if password_result != ():
            profile_id = password_result[0]['profile_id']
            set_session(profile_id)
            #main_screen.withdraw()
            #main_screen.deiconify()
            login_sucess_form(profile_id)
        else:
            password_not_recognised()
    else:
        user_not_found()

# Designing popup for login success

def login_sucess_form(profile_id):
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
 
def user_profile_form():
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

    user_details = f"""Name: {fullname}
Gender: {gender}
Age: {age}
Height: {height}
Body Weight: {bodyweight}
Meal Number: {meal_number}
Activity Level: {activity_level}"""

    global user_profile_screen
    user_profile_screen = Toplevel(main_screen)
    user_profile_screen.title("User Details")
    user_profile_screen.geometry("350x250")
    user_profile_screen.columnconfigure(0, weight=350)

    original = PIL.Image.open("imgs/shaon.jpg")
    size = (100, 100)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)
    #display = Canvas(main_screen, bd=0, highlightthickness=0)
    #display.create_image(0, 0, image=img, anchor=NW, tags="IMG")
    #display.pack()
    Label(user_profile_screen,text="User Details", bg="#969ba3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    pro_pic_frame = Frame(user_profile_screen, bg = '#a7abb2', relief=RAISED, borderwidth=1)
    pro_pic_frame.grid(row=1,sticky="nesw")
    panel = Label(pro_pic_frame,text=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    panel.image = img
    panel.grid(rowspan=7,column=0,sticky="nesw")

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
    
    Label(pro_pic_frame,text="Gender :", width=11, anchor="w", bg='#b5aba4').grid(row=1,column=1,sticky="w")
    Label(pro_pic_frame,text="Age :", width=11, anchor="w", bg='#b5aba4').grid(row=2,column=1,sticky="w")
    Label(pro_pic_frame,text="Height :", width=11, anchor="w", bg='#b5aba4').grid(row=3,column=1,sticky="w")
    Label(pro_pic_frame,text="Bodyweight :", width=11, anchor="w", bg='#b5aba4').grid(row=4,column=1,sticky="w")
    Label(pro_pic_frame,text="Meal Number :", width=11, anchor="w", bg='#b5aba4').grid(row=5,column=1,sticky="w")
    Label(pro_pic_frame,text="Activity Level :", width=11, anchor="w", bg='#b5aba4').grid(row=6,column=1,sticky="w")

    Label(pro_pic_frame,textvariable=gender, width =5, bg='#c1b3aa').grid(row=1,column=2,sticky="w")
    Label(pro_pic_frame,textvariable=age, width =5, bg='#c1b3aa').grid(row=2,column=2,sticky="w")
    Label(pro_pic_frame,textvariable=height, width =5, bg='#c1b3aa').grid(row=3,column=2,sticky="w")
    Label(pro_pic_frame,textvariable=bodyweight, width =5, bg='#c1b3aa').grid(row=4,column=2,sticky="w")
    Label(pro_pic_frame,textvariable=meal_number, width =5, bg='#c1b3aa').grid(row=5,column=2,sticky="w")
    Label(pro_pic_frame,textvariable=activity_level, width =5, bg='#c1b3aa').grid(row=6,column=2,sticky="w")

    #panel2 = Label(pro_pic_frame,text=user_details, bg='red')
    #panel2.grid(row=1,column=1,sticky="nesw")
    Button(user_profile_screen,text="Add/Edit details", height="2", width="30", command = add_profile_details).grid(row=2,sticky="nesw")
    

    
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()
    user_profile_form()

 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")


    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()

"""
Flow list
1. Activate email and verify
"""