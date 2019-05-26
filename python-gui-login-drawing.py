from tkinter import *

def draw_profile_information_section_frame():
    profile_information_frame = Frame(application_screen, bg = '#969ba3', relief=RAISED, borderwidth=1, height=Section_Height, width=Section_Width)

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
        
def draw_sleep_section_frame():
    sleep_colors = {
        'primary_hex' : '#74909e',#'#9cc1d6'
        'header_title_hex' : 'LightSkyBlue3',
    }
    global Sleep_Section_Container_Frame
    global Current_Date_Bed_Var
    global Current_Date_Awake_Var
    global Sleep_Required_Minimum_Var
    global Sleep_Deficit_Var
    
    global Sleep_Start_Entry
    global Sleep_Gateup_Entry
    global Sleep_Required_Minimum_Entry

    Sleep_Section_Container_Frame = Frame(application_screen, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)
    
    
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
    

    Sleep_Section_Active_Container_Frame = Frame(Sleep_Section_Container_Frame, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1)
    Sleep_Section_Active_Container_Frame.grid(sticky="nesw")
    #Sleep_Section_Active_Container_Frame.grid_propagate(False)
    Sleep_Section_Active_Container_Frame.columnconfigure(0, weight=Section_Width)

    Sleep_Section_Inactive_Container_Frame = Frame(Sleep_Section_Container_Frame, bg = sleep_colors['primary_hex'], relief=RAISED, borderwidth=1)
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
    exercise_colors = {
        'primary_hex' : '#e49a4b',
        'header_title_hex' : '#d78b3a',
    }
    global Exercise_Section_Container_Frame
    Exercise_Section_Container_Frame = Frame(application_screen, bg = exercise_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

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

    Label(Exercise_Section_Active_Container_Frame, text="Sleep Section", bg="LightSkyBlue3", height="2", font=("Calibri", 13)).grid(row=0,sticky="nesw")
    Button(Exercise_Section_Active_Container_Frame, text="Exercise Section \u25E4 Hide", bg=exercise_colors['header_title_hex'], height=2, font=("Calibri", 13), command=toggle_section).grid(row=0,sticky="nesw")
    #image_panel = Label(profile_information_holder, textvariable=fullname, compound = 'top',font=("Helvetica", 8), bg='#7e9189', anchor="nw", height = 100, image = img)
    Inactive_Button = Button(Exercise_Section_Inactive_Container_Frame, text="Click to Expand\u25E2", command=toggle_section, height=Section_Height, anchor="center", bg=exercise_colors['primary_hex'], image=img,compound="top", fg="#23617b", font=("Rockwell Extra Bold", 13))
    Inactive_Button.grid(row=0,sticky="nesw")
    Inactive_Button.image = img


    return Exercise_Section_Container_Frame

def draw_nutrition_section_frame():
    nutrition_colors = {
        'primary_hex' : '#a2c950',
        'header_title_hex' : '#99ba55',
    }

    global Nutrition_Section_Container_Frame
    Nutrition_Section_Container_Frame = Frame(application_screen, bg = nutrition_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

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

def draw_grooming_section_frame():
    grooming_colors = {
        'primary_hex' : '#cea3c2',
        'header_title_hex' : 'LightSkyBlue3'
    }
    global Grooming_Section_Container_Frame
    Grooming_Section_Container_Frame = Frame(application_screen, bg = grooming_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

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


def draw_finance_section_frame():
    finance_colors = {
        'primary_hex' : '#d8b80d',
        'header_title_hex' : 'LightSkyBlue3',
    }
    global Finance_Section_Container_Frame
    Finance_Section_Container_Frame = Frame(application_screen, bg = finance_colors['primary_hex'], relief=RAISED, borderwidth=1, width=Section_Width, height=Section_Height)

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

