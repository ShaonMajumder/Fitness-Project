from working import *

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
    
    New_Exercise_Form = Toplevel(top_frame)
    New_Exercise_Form.geometry("400x400")
    Label(New_Exercise_Form, text="Exercise Name").pack()

    New_Exercise_Name_Entry = Entry(New_Exercise_Form)
    New_Exercise_Name_Entry.pack(padx=5)
    Label(New_Exercise_Form, text="Target Bodypart").pack()
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
    Label(New_Exercise_Form, text="Type-").pack()
    
    New_Exercise_Type_Entry = AutocompleteEntry(['isolation','compound','freehand','cardio'], New_Exercise_Form, bd = 2, width=15)
    New_Exercise_Type_Entry.pack(padx=5)
    Label(New_Exercise_Form, text="Instrument-").pack()
    #query = "Select * From `exercise_instruments`"
    result = mydb.select("*","","exercise_instruments")
    
    New_Exercise_Instrument_Entry = AutocompleteEntry([line['name'] for line in result], New_Exercise_Form, bd = 2, width=15)
    New_Exercise_Instrument_Entry.pack(padx=5)
    Label(New_Exercise_Form, text="Comment").pack()
    
    New_Exercise_Comment_Entry = Entry(New_Exercise_Form)
    New_Exercise_Comment_Entry.pack(padx=5)
    New_Exercise_Submit_Button = Button(New_Exercise_Form, text="Submit", command=New_Exercise_Entry_Form_ok)
    New_Exercise_Submit_Button.pack()


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
    Button(profile_information_holder,text="Change", bg="#b1b5b2", command = select_file).grid(row=6,column=0,sticky="w")
    #Button(profile_information_holder,text="Change", command = lambda: select_file(new_propic_filename)).grid(row=6,column=0,sticky="w")

    Button(profile_information_frame,text="Add/Edit details", height="2", width="30", bg="#b1b5b2", command = add_profile_details_form).grid(row=2,sticky="nesw")
    return profile_information_frame
        

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
    Button(Exercise_Section_Active_Container_Frame, text="Add New Exercise", command=lambda: New_Exercise_Entry_Form(top_frame) ).grid(row=1,sticky="nesw")

    return Exercise_Section_Container_Frame

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

    img = image_to_tkinter_img(profile_picture_folder + 'nutrition.png', (200, 200))
    
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
    
    img = image_to_tkinter_img(profile_picture_folder + 'grooming.png', (200, 200))

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

    img_ = image_to_tkinter_img(profile_picture_folder + 'hygene.png',(130, 130))
    
    Hygene_ = Button(Hygene_Section_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, anchor="center", bg=grooming_colors['header_title_hex'], image=img_, compound="top", fg="#23617b", font=("Rockwell Extra Bold", 11), height=Section_Body_Height-50, width=Section_Width//2)
    Hygene_.grid(sticky="w")
    Hygene_.image = img_

    img_ = image_to_tkinter_img(profile_picture_folder + 'dressing.png', (130, 130))

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

    img = image_to_tkinter_img(profile_picture_folder + 'finance.png',(200, 200))
    
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

    profile_picture_folder="imgs/"
    if profile_picture == "":
        img_file = "profile_avatar.png"
    else:
        img_file = profile_picture
    
    profile_img = image_to_tkinter_img(profile_picture_folder + img_file,(90, 90))

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

def exercise_module_frame(top_frame):
    return draw_exercise_section_frame(top_frame)

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