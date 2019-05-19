u_config = read_config_ini("youtube_config.ini")

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

def get_site_title(url):
	page = get_html(url)
	YouTube_title = page.title.text.replace(" - YouTube","")
	return YouTube_title

def list_utbube_title(lines):
	#lines = read_file(filename)
	return [get_site_title(url) + utube_title_seperating_flag + url for url in lines]	

def find_tag_in_list(target_li,tag):
	return [stri for stri in target_li if tag in stri]

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

def repair_data_file():
	lines = read_file(Get_utube_video_title_Input_File_Name)
	lines = [line for line in lines if line != '']
	stri = '\n'.join(lines)
	write_file(Get_utube_video_title_Input_File_Name, stri, mode )
	messagebox.showinfo( "Hello Python", "Data File repaired.")


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

#query = "SELECT `value` FROM `constants` where `name` = 'Resource_Categories'"
search_result = mydb.select(['value'],"`name` = 'Resource_Categories'","constants")
OPTIONS = [line['value'] for line in search_result][0].split(',')
OPTIONS.append('NEW')