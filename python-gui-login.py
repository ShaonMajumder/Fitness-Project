#import modules
 
from tkinter import *
from utilities.utility import *
from utilities.mysql_database import *
import os
import hashlib

utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")

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
 
    Label(login_screen, text="Username * ").pack()
    email_login_entry = Entry(login_screen, textvariable=email_verify)
    email_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
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
            login_sucess()
        else:
            password_not_recognised()
    else:
        user_not_found()

# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
 
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