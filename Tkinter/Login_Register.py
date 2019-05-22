from tkinter import *
from tkinter import messagebox
from utilities.utility import *
from utilities.mysql_database import *
import hashlib

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


tkinter_config = read_config_ini("Tkinter/Tkinter_Config.ini")


class Login_Register(object):
    """docstring for ClassName"""
    def __init__(self,*args, **kwargs):
        ## object,iconfile
        iconfile = kwargs['icon']
        self.destroy_session()
        #if needed use existing global session_data instead of empty dictionary
        self.success_function = kwargs['success_function']


        if 'object' in kwargs:
            #   type(Toplevel(Tk())).__name__ == 'Toplevel'
            object_ = kwargs['object']
            login_register_home_screen = Toplevel(object_)
        else:
            #  if type(object_).__name__ == 'Tk':
            login_register_home_screen = Tk()
            login_register_home_screen.iconbitmap(iconfile)

        form_size = tkinter_config['LOGIN_REGISTER_MAIN']['form_size']
        form_title = tkinter_config['LOGIN_REGISTER_MAIN']['title']
        form_background_color = tkinter_config['LOGIN_REGISTER_MAIN']['form_background_color']
        project_title = tkinter_config['LOGIN_REGISTER_MAIN']['project_title']
        login_button_title = tkinter_config['LOGIN_REGISTER_MAIN']['login_button_title']
        register_button_title = tkinter_config['LOGIN_REGISTER_MAIN']['register_button_title']

        login_register_home_screen.geometry(form_size)
        login_register_home_screen.title(form_title)
        login_register_home_screen.configure(background=form_background_color)

        Label(text=project_title, bg="#715E4E", fg='white', width="300", height="2", font=("Calibri", 13)).pack()
        Button(text=login_button_title, bg='#818A6F', fg='white', height="2", width="30", command = lambda: self.login()).pack(pady=20)
        Button(text=register_button_title, bg='#52733B', fg='white', height="2", width="30", command = lambda: self.register()).pack()
        self.frame = login_register_home_screen

    def register_user(self):
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
 
    def login_verify(self):
        email1 = self.email_verify.get()
        password1 = self.password_verify.get()
        password_result = hashlib.md5(password1.encode())
        password1 = password_result.hexdigest()
        email_login_entry = self.email_login_entry
        password_login_entry = self.password_login_entry
        email_login_entry.delete(0, END)
        password_login_entry.delete(0, END)

        username_result = mydb.select('*',f"""`email`='{email1}'""","profiles")
        if username_result != ():
            password_result = mydb.select('*',f"""`password`='{password1}'""","profiles")
            if password_result != ():
                profile_id = password_result[0]['profile_id']
                self.set_session(profile_id)
                self.login_screen.destroy()
                messagebox.showinfo("Fitness-Project", "You are successfully logged in.")
                
                #login_register_home_screen.withdraw()
                #login_register_home_screen.deiconify()

                #self.success_function()
                self.frame.destroy()
                
                
            else:
                messagebox.showinfo("Fitness-Project", "Password does not match.")
        else:
            messagebox.showinfo("Fitness-Project", "This email is not registered with us.\nEnter your correct email.")

    def register(self):
        #global register_screen
        register_screen = Toplevel(login_register_home_screen)
        register_screen.title("Register")
        register_screen.geometry("300x250")

        #global username
        #global password
        #global email
        #global username_entry
        #global password_entry
        #global email_entry
        
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
        Button(register_screen, text="Register", width=10, height=1, bg="blue", command = lambda: self.register_user()).pack()
        self.register_screen = register_screen
        self.username = username
        self.password = password
        self.email = email
        self.username_entry = username_entry
        self.password_entry = password_entry
        self.email_entry = email_entry

    def login(self):
        #global login_screen
        login_screen = Toplevel(self.frame)
        login_screen.title("Login")
        login_screen.geometry("300x250")
        Label(login_screen, text="Please enter details below to login").pack()
        Label(login_screen, text="").pack()
     
        #global email_verify
        #global password_verify
     
        email_verify = StringVar()
        password_verify = StringVar()
     
        #global email_login_entry
        #global password_login_entry
     
        Label(login_screen, text="Email * ").pack()
        email_login_entry = Entry(login_screen, textvariable=email_verify)
        email_login_entry.pack()
        Label(login_screen, text="").pack()
        Label(login_screen, text="Password * ").pack()
        password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
        password_login_entry.pack()
        Label(login_screen, text="").pack()
        Button(login_screen, text="Login", width=10, height=1, command = lambda: self.login_verify()).pack()
        self.login_screen = login_screen
        self.email_verify = email_verify
        self.password_verify = password_verify
        self.email_login_entry = email_login_entry
        self.password_login_entry = password_login_entry
    def is_login(self):
        return self.login_state
    def set_session(self,profile_id):
        self.login_state = True
        self.session_data = {'profile_id': profile_id}
    def destroy_session(self):
        self.login_state = False
        self.session_data = {}

