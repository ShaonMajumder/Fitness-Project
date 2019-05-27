from working import *

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

        img = image_to_tkinter_img(image_folder + 'sleep_section2.png', (200, 200))
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



def add_profile_details_form():
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

    def processing():
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

    def draw():
        global add_profile_details_screen
        global fullname_entry
        global gender_entry
        global age_entry
        global birthdate_entry
        global protein_grams_per_body_pound_entry
        global height_entry
        global bodyweight_entry
        global meal_number_entry
        global activity_level_entry

        add_profile_details_screen = Toplevel(application_screen)
        add_profile_details_screen.title("Add/Edit details")
        add_profile_details_screen.geometry("300x500")

        Label(add_profile_details_screen, text="Please enter details below").pack()
        Label(add_profile_details_screen, text="").pack()    
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
    processing()
    draw()

## Processing
### Processing
## Draw
def draw_profile_information_section_frame(top_frame):
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

    profile_information_frame = Frame(top_frame, bg = '#969ba3', relief=RAISED, borderwidth=1, height=Section_Height, width=Section_Width)

    Label(profile_information_frame,text="User Details", bg="#969ba3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    profile_information_holder = Frame(profile_information_frame, bg = '#a7abb2', relief=RAISED, borderwidth=1)
    profile_information_holder.grid(row=1,sticky="nesw")

    image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = profile_img)
    image_panel.image = profile_img
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
    Button(profile_information_holder,text='Export Text',bg='#b1b5b2',width=8).grid(row=5,column=3,padx=4,sticky="w")
    Button(profile_information_holder,text='Print',bg='#b1b5b2',width=8).grid(row=6,column=3,padx=4,sticky="w")

    Button(profile_information_holder,text="Change", bg="#b1b5b2", command = select_file).grid(row=6,column=0,sticky="w")
    #Button(profile_information_holder,text="Change", command = lambda: select_file(new_propic_filename)).grid(row=6,column=0,sticky="w")

    Button(profile_information_frame,text="Add/Edit details", height="2", width="30", bg="#b1b5b2", command = add_profile_details_form).grid(row=2,sticky="nesw")
    return profile_information_frame
        


def draw_nutrition_section_frame(top_frame):
    nutrition_colors = {
        'primary_hex' : '#a2c950',
        'header_title_hex' : '#99ba55',
    }

    global Nutrition_Section_Container_Frame
    Nutrition_Section_Container_Frame = Frame(top_frame, bg = nutrition_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

    @static_var("status", 'active')
    def toggle_section():
        if toggle_section.status == 'hidden':
            Nutrition_Section_Active_Container_Frame.grid()
            Nutrition_Section_Inactive_Container_Frame.grid_remove()
            toggle_section.status = 'active'
        elif toggle_section.status == 'active':
            Nutrition_Section_Active_Container_Frame.grid_remove()
            Nutrition_Section_Inactive_Container_Frame.grid()
            toggle_section.status = 'hidden'
    

    Nutrition_Section_Active_Container_Frame = Frame(Nutrition_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Nutrition_Section_Active_Container_Frame.grid(sticky="nesw")
    #Nutrition_Section_Active_Container_Frame.grid_propagate(False)
    Nutrition_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Nutrition_Section_Inactive_Container_Frame = Frame(Nutrition_Section_Container_Frame, bg = nutrition_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Nutrition_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Nutrition_Section_Inactive_Container_Frame.grid_propagate(False)
    Nutrition_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_section()

    img = image_to_tkinter_img(image_folder + 'nutrition.png', (200, 200))
    
    Label(Nutrition_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Nutrition_Section_Active_Container_Frame, text="Nutrition Section \u25E4 Hide", command=toggle_section, height=2,bg=nutrition_colors['header_title_hex'],font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Nutrition_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=nutrition_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img

    return Nutrition_Section_Container_Frame

def draw_grooming_section_frame(top_frame):
    grooming_colors = {
        'primary_hex' : '#cea3c2',
        'header_title_hex' : 'LightSkyBlue3'
    }
    global Grooming_Section_Container_Frame
    Grooming_Section_Container_Frame = Frame(top_frame, bg = grooming_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

    @static_var("status", 'active')
    def toggle_section():
        if toggle_section.status == 'hidden':
            Grooming_Section_Active_Container_Frame.grid()
            Grooming_Section_Inactive_Container_Frame.grid_remove()
            toggle_section.status = 'active'
        elif toggle_section.status == 'active':
            Grooming_Section_Active_Container_Frame.grid_remove()
            Grooming_Section_Inactive_Container_Frame.grid()
            toggle_section.status = 'hidden'


    Grooming_Section_Active_Container_Frame = Frame(Grooming_Section_Container_Frame, bg = grooming_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Grooming_Section_Active_Container_Frame.grid(sticky="nesw")
    #Grooming_Section_Active_Container_Frame.grid_propagate(False)
    Grooming_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Grooming_Section_Inactive_Container_Frame = Frame(Grooming_Section_Container_Frame, bg = grooming_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Grooming_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Grooming_Section_Inactive_Container_Frame.grid_propagate(False)
    Grooming_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    
    
    toggle_section()
    
    img = image_to_tkinter_img(image_folder + 'grooming.png', (200, 200))

    Label(Grooming_Section_Active_Container_Frame, text="Grooming Section", bg=grooming_colors['header_title_hex'], height=1, font=("Calibri", 13), borderwidth=0).grid(row=0,sticky="nesw")
    Button(Grooming_Section_Active_Container_Frame, text="Grooming Section \u25E4 Hide", command=toggle_section, height=1, bg=grooming_colors['header_title_hex'],font=("Calibri", 13), borderwidth=0).grid(row=0,sticky="nesw")

    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Grooming_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=grooming_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img

    Grooming_Section_Sub_Container_Frame = Frame(Grooming_Section_Active_Container_Frame,bg='black', relief=RAISED, borderwidth=1)
    Grooming_Section_Sub_Container_Frame.grid(sticky="nesw", row = 2)
    Sub_Header_Frame = Frame(Grooming_Section_Active_Container_Frame, bg='red', relief=RAISED, borderwidth=0, height=0.5, width=Section_Width)
    Sub_Header_Frame.grid(row=1,sticky="nesw")
    Hygene_Section_Container_Frame = Frame(Grooming_Section_Sub_Container_Frame,bg='LightSkyBlue3', relief=RAISED, borderwidth=1, height=Section_Body_Height, width=Section_Width//2)
    Dressing_Section_Container_Frame = Frame(Grooming_Section_Sub_Container_Frame,bg=grooming_colors['primary_hex'], relief=RAISED, borderwidth=1, height=Section_Body_Height, width=Section_Width//2)
    Hygene_Section_Container_Frame.grid(sticky="w", row = 1, column = 0)
    Dressing_Section_Container_Frame.grid(sticky="w", row = 1, column = 1)

    img_ = image_to_tkinter_img(image_folder + 'hygene.png',(130, 130))
    
    Hygene_ = Button(Hygene_Section_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, anchor="center", bg=grooming_colors['header_title_hex'], image=img_, compound="top", fg="#23617b", font=("Rockwell Extra Bold", 11), height=Section_Body_Height-50, width=Section_Width//2)
    Hygene_.grid(sticky="w")
    Hygene_.image = img_

    img_ = image_to_tkinter_img(image_folder + 'dressing.png', (130, 130))

    Dressing_ = Button(Dressing_Section_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, anchor="center", bg=grooming_colors['primary_hex'], image=img_, compound="top", fg="#23617b", font=("Rockwell Extra Bold", 11), height=Section_Body_Height-50, width=Section_Width//2)
    Dressing_.grid(sticky="w")
    Dressing_.image = img_

    Sub_Header_Inactive_Width = 124
    @static_var("status", 'initial')
    def toggle_sub_section():
        if toggle_sub_section.status == 'initial':
            Sub_Header_Frame.columnconfigure(0, weight=Section_Width//2)
            Sub_Header_Frame.columnconfigure(1, weight=Section_Width//2)
            Hygene_Header.config(borderwidth=1,width=Section_Width//2)
            Dressing_Header.config(borderwidth=1,width=Section_Width//2)
            toggle_sub_section.status = 'active'
        elif toggle_sub_section.status == 'hidden':
            Sub_Header_Frame.columnconfigure(0, weight=Sub_Header_Inactive_Width)
            Sub_Header_Frame.columnconfigure(1, weight=Section_Width - Sub_Header_Inactive_Width)
            Hygene_Header.config(borderwidth=0,width=Sub_Header_Inactive_Width)
            Dressing_Header.config(borderwidth=1,width=Section_Width - Sub_Header_Inactive_Width)
            Dressing_Section_Container_Frame.config(width=Section_Width)
            Dressing_Section_Container_Frame.grid()
            Hygene_Section_Container_Frame.grid_remove()
            Hygene_.grid_remove()
            Dressing_.grid_remove()
            toggle_sub_section.status = 'active'
        elif toggle_sub_section.status == 'active':
            Sub_Header_Frame.columnconfigure(0, weight=Section_Width - Sub_Header_Inactive_Width)
            Sub_Header_Frame.columnconfigure(1, weight=Sub_Header_Inactive_Width)
            Hygene_Header.config(borderwidth=1,width=Section_Width - Sub_Header_Inactive_Width)
            Dressing_Header.config(borderwidth=0,width=Sub_Header_Inactive_Width)
            Hygene_Section_Container_Frame.config(width=Section_Width)
            Dressing_Section_Container_Frame.grid_remove()
            Hygene_Section_Container_Frame.grid()
            Hygene_.grid_remove()
            Dressing_.grid_remove()
            toggle_sub_section.status = 'hidden'

    Hygene_Header = Button(Sub_Header_Frame, text="Hygene Section", command=toggle_sub_section, bg=grooming_colors['header_title_hex'],font=("Calibri", 13), borderwidth=0, relief=RAISED)
    Hygene_Header.grid(row=0,column=0,sticky="ns") #117
    Dressing_Header = Button(Sub_Header_Frame, text="Dressing Section", command=toggle_sub_section, bg=grooming_colors['primary_hex'],font=("Calibri", 13), borderwidth=0, relief=RAISED)
    Dressing_Header.grid(row=0,column=1,sticky="ns") #124
    
    toggle_sub_section()

    return Grooming_Section_Container_Frame


def draw_finance_section_frame(top_frame):
    finance_colors = {
        'primary_hex' : '#d8b80d',
        'header_title_hex' : 'LightSkyBlue3',
    }
    global Finance_Section_Container_Frame
    Finance_Section_Container_Frame = Frame(top_frame, bg = finance_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

    @static_var("status", 'active')
    def toggle_section():
        if toggle_section.status == 'hidden':
            Finance_Section_Active_Container_Frame.grid()
            Finance_Section_Inactive_Container_Frame.grid_remove()
            toggle_section.status = 'active'
        elif toggle_section.status == 'active':
            Finance_Section_Active_Container_Frame.grid_remove()
            Finance_Section_Inactive_Container_Frame.grid()
            toggle_section.status = 'hidden'
    

    Finance_Section_Active_Container_Frame = Frame(Finance_Section_Container_Frame, bg = finance_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Finance_Section_Active_Container_Frame.grid(sticky="nesw")
    #Finance_Section_Active_Container_Frame.grid_propagate(False)
    Finance_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Finance_Section_Inactive_Container_Frame = Frame(Finance_Section_Container_Frame, bg = '#9cc1d6', relief=RAISED, borderwidth=1)
    Finance_Section_Inactive_Container_Frame.grid(sticky="nesw")
    #Finance_Section_Inactive_Container_Frame.grid_propagate(False)
    Finance_Section_Inactive_Container_Frame.columnconfigure(0, weight=Section_Width)
    
    toggle_section()

    img = image_to_tkinter_img(image_folder + 'finance.png',(200, 200))
    
    Label(Finance_Section_Active_Container_Frame, text="Sleep Section", bg=finance_colors['header_title_hex'], height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Finance_Section_Active_Container_Frame, text="Sleep Section \u25E4 Hide", command=toggle_section, height=2,bg=finance_colors['header_title_hex'],font=("Calibri", 13)).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Finance_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=finance_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img

    return Finance_Section_Container_Frame
### Draw

def profile_information_module_frame(top_frame):
    global session_data
    global fullname
    global gender
    global age
    global height
    global bodyweight
    global meal_number
    global activity_level
    global profile_img

    profile_id = session_data['profile_id']
    results = mydb.execute(f"""SELECT * FROM biodata INNER JOIN profiles ON biodata.profile_id = profiles.profile_id WHERE profiles.`profile_id` = '{profile_id}'""")
    row = results[0]
    profile_picture = row['profile_picture']

    image_folder="imgs/"
    if profile_picture == "":
        img_file = "profile_avatar.png"
    else:
        img_file = profile_picture
    
    profile_img = image_to_tkinter_img(image_folder + img_file,(90, 90))

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
    
    return  draw_profile_information_section_frame(top_frame)



def finance_module_frame(top_frame):
    return draw_finance_section_frame(top_frame)

def grooming_module_frame(top_frame):
    return draw_grooming_section_frame(top_frame)

def nutrition_module_frame(top_frame):
    return draw_nutrition_section_frame(top_frame)


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
    application_screen.geometry(str(Section_Width*n_columns) + "x" + str(Section_Height*n_rows))
    tkinter_center(application_screen)
    top_frame = application_screen

    #application_screen.columnconfigure(0, weight=Section_Width)
    #application_screen.columnconfigure(1, weight=Section_Width)

    profile_information_frame = profile_information_module_frame(top_frame)
    sleep_section_obj = sleep_section_class(top_frame)
    sleep_section_frame = sleep_section_obj.first_appearance()

    exercise_section_frame = exercise_module_frame(top_frame)
    nutrition_section_frame = nutrition_module_frame(top_frame)
    grooming_section_frame = grooming_module_frame(top_frame)
    finance_section_frame = finance_module_frame(top_frame)

    profile_information_frame.grid(sticky="nesw", row=0, column=0)
    sleep_section_frame.grid(sticky="nesw", row = 0, column = 1)
    exercise_section_frame.grid(sticky="nesw", row = 0, column = 2)
    finance_section_frame.grid(sticky="nesw", row = 1, column = 0)
    grooming_section_frame.grid(sticky="nesw", row = 1, column = 1)
    nutrition_section_frame.grid(sticky="nesw", row = 1, column = 2)
    
    

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
    finance_section_frame.grid_propagate(False)
    finance_section_frame.columnconfigure(0, weight=Section_Width)

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