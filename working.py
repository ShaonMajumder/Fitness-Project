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


class sleep_section_class:
    def __init__(self,top_frame):
        self.top_frame = top_frame

    def first_appearance(self):
        self.intial_processing()
        sleep_frame = self.draw()
        return sleep_frame

    def intial_processing(self):
        time_show_format = 'd/m/y <h>:<m>AM'
        self.Current_Date_Bed_Var = StringVar()
        self.Current_Date_Awake_Var = StringVar()
        self.Sleep_Required_Minimum_Var = StringVar()
        self.Sleep_Deficit_Var = StringVar()
        
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
            bed_time = time_show_format
            wakeup_time = time_show_format
        elif last_result['todays_slept_time'] != '0000-00-00 00:00:00':     
            min_req_time = str(last_result['min_required_sleep_time'])
            overall_sleep_excess_or_deficit_time = last_result['overall_sleep_excess_or_deficit_time']
            if overall_sleep_excess_or_deficit_time == '': overall_sleep_excess_or_deficit_time = '0hours'
            bed_time = time_show_format
            wakeup_time = time_show_format
        else:
            min_req_time = str(last_result['min_required_sleep_time'])
            overall_sleep_excess_or_deficit_time = last_result['overall_sleep_excess_or_deficit_time']
            if overall_sleep_excess_or_deficit_time == '': overall_sleep_excess_or_deficit_time = '0hours'
            
            if last_result['bed_time'] != '0000-00-00 00:00:00':
                bed_time = last_result['bed_time'].strftime("%d/%m/%y %I:%M%p")
                wakeup_time = time_show_format
            elif last_result['wakeup_time'] != '0000-00-00 00:00:00':
                wakeup_time = last_result['wakeup_time'].strftime("%d/%m/%y %I:%M%p")
                bed_time = time_show_format

        self.Current_Date_Bed_Var.set(bed_time)
        self.Current_Date_Awake_Var.set(wakeup_time)        
        self.Sleep_Required_Minimum_Var.set(min_req_time)
        self.Sleep_Deficit_Var.set(overall_sleep_excess_or_deficit_time)

    def draw(self):
        sleep_colors = {
            'primary_hex' : '#74909e',#'#9cc1d6'
            'header_title_hex' : 'LightSkyBlue3',
        }

        self.Sleep_Section_Container_Frame = Frame(self.top_frame, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

        @static_var("status", 'active')
        def toggle_section():
            if toggle_section.status == 'hidden':
                Sleep_Section_Active_Container_Frame.grid()
                Sleep_Section_Inactive_Container_Frame.grid_remove()
                toggle_section.status = 'active'
            elif toggle_section.status == 'active':
                Sleep_Section_Active_Container_Frame.grid_remove()
                Sleep_Section_Inactive_Container_Frame.grid()
                toggle_section.status = 'hidden'
        

        Sleep_Section_Active_Container_Frame = Frame(self.Sleep_Section_Container_Frame, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1)
        Sleep_Section_Active_Container_Frame.grid(sticky="nesw")
        #Sleep_Section_Active_Container_Frame.grid_propagate(False)
        Sleep_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

        Sleep_Section_Inactive_Container_Frame = Frame(self.Sleep_Section_Container_Frame, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1)
        Sleep_Section_Inactive_Container_Frame.grid(sticky="nesw")
        #Sleep_Section_Inactive_Container_Frame.grid_propagate(False)
        Sleep_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
        
        toggle_section()

        img = image_to_tkinter_img(profile_picture_folder + 'sleep_section2.png', (200, 200))
        Label(Sleep_Section_Active_Container_Frame, text="Sleep Section", bg=sleep_colors['header_title_hex'], height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
        Button(Sleep_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_section, height=2,bg=sleep_colors['header_title_hex'],font=("Calibri", 13)).grid(row=0,sticky="nesw")
        #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
        Inactive_Button = Button(Sleep_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=sleep_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
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
        self.Sleep_Start_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=self.Current_Date_Bed_Var, bg=bglabelentry)
        self.Sleep_Start_Entry.grid(sticky="w",row=0,column=1)
        self.Sleep_Gateup_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=self.Current_Date_Awake_Var, bg=bglabelentry)
        self.Sleep_Gateup_Entry.grid(sticky="w",row=1,column=1)
        self.Sleep_Required_Minimum_Entry = Entry(sleep_info_frame, bd = 2,width=32, textvariable=self.Sleep_Required_Minimum_Var, bg=bglabelentry)
        self.Sleep_Required_Minimum_Entry.grid(sticky="w",row=2,column=1)
        Sleep_Deficit_Label = Label(sleep_info_frame, width=27, textvariable = self.Sleep_Deficit_Var, bg=bglabelentry)
        Sleep_Deficit_Label.grid(sticky="w",row=3,column=1)
            
        Button(Sleep_Section_Active_Container_Frame, text="Submit", command=self.sleep_form_submit,height=2,bg="#b1d2e0").grid(sticky="nesw", row=7 )
        
        Recovery_or_Less_Time_Label = Label(sleep_info_frame, text = "Extra Recovery Sleep Time Allowed-")
        Recovery_or_Less_Time_Entry = Entry(sleep_info_frame, bd = 2,width=15)
        
        return self.Sleep_Section_Container_Frame

    def sleep_form_submit(self):
        time_show_format = 'd/m/y <h>:<m>AM'
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

        bedtime = self.Sleep_Start_Entry.get()
        gateuptime = self.Sleep_Gateup_Entry.get()
        reqtime_ = self.Sleep_Required_Minimum_Entry.get()
        reqtime = str2deltatime(reqtime_)
                

        if last_result == ():
            if bedtime != time_show_format and gateuptime != time_show_format:
                try:
                    bedtime_obj = datetime.datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
                except ValueError:
                    bedtime_obj = datetime.datetime.strptime(bedtime, '%d/%m/%Y %I:%M%p')
                try:
                    gateuptime_obj = datetime.datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
                except ValueError:
                    gateuptime_obj = datetime.datetime.strptime(gateuptime, '%d/%m/%Y %I:%M%p')
                            
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

            elif bedtime != time_show_format:
                bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
                bedtime = str(bedtime_obj)
                mydb.insert(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"sleep_data")
            elif gateuptime != time_show_format:
                gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
                gateuptime = str(gateuptime_obj)
                mydb.insert(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"sleep_data")


        elif last_result['todays_slept_time'] != '0000-00-00 00:00:00':
            if bedtime != time_show_format and gateuptime != time_show_format:
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

            elif bedtime != time_show_format:
                bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
                bedtime = str(bedtime_obj)
                mydb.insert(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"sleep_data")
            elif gateuptime != time_show_format:
                gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
                gateuptime = str(gateuptime_obj)
                mydb.insert(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"sleep_data")

        else:
            if bedtime != time_show_format and gateuptime != time_show_format:
                try:
                    bedtime_obj = datetime.datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
                except ValueError:
                    bedtime_obj = datetime.datetime.strptime(bedtime, '%d/%m/%Y %I:%M%p')
                try:
                    gateuptime_obj = datetime.datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
                except ValueError:
                    gateuptime_obj = datetime.datetime.strptime(gateuptime, '%d/%m/%Y %I:%M%p')
                
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

            elif bedtime != time_show_format:
                bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
                bedtime = str(bedtime_obj)
                mydb.edit(['bed_time','min_required_sleep_time'],[bedtime,reqtime_],"`id` = "+str(last_result['id']),"sleep_data")
            elif gateuptime != time_show_format:
                gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
                gateuptime = str(gateuptime_obj)
                mydb.edit(['wakeup_time','min_required_sleep_time'],[gateuptime,reqtime_],"`id` = "+str(last_result['id']),"sleep_data")

        #self.Sleep_Section_Container_Frame.destroy()
        self.Current_Date_Bed_Var.set('')
        self.Current_Date_Awake_Var.set('')
        self.Sleep_Required_Minimum_Var.set('')
        messagebox.showinfo("Sleep Section","Your sleep recorded.")
