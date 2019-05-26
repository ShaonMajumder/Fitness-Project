from tkinter import *
from datetime import timedelta
import re
import random
import string
import configparser
import codecs
import os
import win32print
import smtplib

time_units = ['years','months','days','hours','minutes','seconds']
time_quan = {'seconds':60, 'minutes':60, 'hours':24, 'days':30, 'months':12, 'years':1}

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def send_email(subject, body, CC, to, sent_from, smtp_user, smtp_password):
    email_text = f"""Subject: {subject}
From: {sent_from}
To: {", ".join(to)}
CC: {CC}\n

{body}"""
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')

    except:  
        print('Something went wrong...')

def unique_items(li):
    dic = {}
    for key in li:
        dic[key] = ''
    unique_keys = [key for key in dic]
    return unique_keys
    
def get_today_day():
    import datetime
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday',  'friday', 'saturday', 'sunday']
    week_day = datetime.datetime.today().weekday()
    day = week_days[week_day]
    return day


def printer_file(filename):
    printer_name = "Canon LBP6030/6040/6018L"
    win32print.SetDefaultPrinter(printer_name)
    os.startfile(filename, "print")

def read_config_ini(filename):
    config = configparser.ConfigParser()
    config.readfp(codecs.open(filename, "r", "utf8"))
    return config

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    for c in range(10):
        letters = letters + str(c)

    return ''.join(random.choice(letters) for i in range(stringLength))

def get_html(url):
    """Returns HTML beautiful soup 4 object"""
    while True:
        try:
            r = requests.get(url=url, timeout=10)
            break
        except ConnectTimeout:
            time.sleep(5)
            alert_tone()
            print("retrying to download page")          
        except ReadTimeout:
            time.sleep(5)
            alert_tone()
            print("retrying to download page")
        except ConnectionError:
            time.sleep(5)
            alert_tone()
            print("retrying to download page")

    r.encoding = r.apparent_encoding
    return BeautifulSoup( r.text, features="html.parser")

def read_file(filename):
	with codecs.open(filename, "r", encoding="utf-8") as file_reader:
		lines = file_reader.readlines()

	ill_chars = ['\r','\n']
	_ = []
	for line in lines:
		for ic in ill_chars:
			line = line.replace(ic,'')
		_.append(line)
	filtered_lines = _
	return filtered_lines

def write_file(filename, strs,mode="w"):
	import codecs
	with codecs.open(filename, mode, encoding='utf-8') as file_appender:
		file_appender.writelines(strs)

def str2deltatime(time_str):
    time_str = simplify_time(time_str)
    time_dic = str2time_dic(time_str)
    time_ = timedelta()
    for c in time_dic:
        if c == "hours":
            time_ = time_ + timedelta(hours=time_dic[c])
        elif c == "minutes":
            time_ = time_ + timedelta(minutes=time_dic[c])
        elif c == "seconds":
            time_ = time_ + timedelta(seconds=time_dic[c])

    return time_

def format_time(time_str,format_str):
    #%H:%M:%S
    time_dic = str2time_dic(time_str)
    format_ref = {'%H':'hours','%M':'minutes','%S':'seconds'}
    format_str = format_str.split(':')
    return_str = []
    for p in format_str:
        if format_ref[p] in time_dic:
            time_digit = time_dic[format_ref[p]]
            return_str.append(add_zeros(time_digit,2))
        else:
            return_str.append("00")

    return ':'.join(return_str)

def add_zeros(time_str,num):
    digit_n = num - len(time_str) #1
    num_ = ""
    for c in range(digit_n):
        num_ = num_ + "0"
    num_ = num_+time_str
    return num_

def divide_num_unit(time_str):
    pos = - 1
    for c in time_str:
        pos = pos + 1
        if c in string.ascii_lowercase:
            return time_str[0:pos], time_str[pos:]

def str2time_dic(time_whole_str):
    #'120years10months15days8hours20minutes90seconds'
    pos = - 1
    chunks = []
    while(pos < len(time_whole_str)-1):
        pos = pos + 1
        C = time_whole_str[pos]
        
        if C in string.ascii_lowercase:
            str_ = ''
            for i in range(pos,len(time_whole_str)):
                k = time_whole_str[i]
                
                if k in string.ascii_lowercase:
                    str_ = str_ + k
                else:
                    break
            
            if str_ in time_units:
                num = time_whole_str[0:pos]
                chunk = num+str_
                time_whole_str = time_whole_str.replace(num+str_,'')
                pos = -1
                
                chunks.append(chunk)
    dic = {}
    for chunk in chunks:
        num, unit = divide_num_unit(chunk)
        dic[unit] = int(float(num))

    return dic


def get_next_key(d,target_key):
    pos = -1
    for key in d:
        pos=pos+1
        if key == target_key:
            listForm = list(d.keys())
            if (pos+1)< len(d):
                return listForm[pos+1]
            else:
                return False

def shorten_time(ordered_dic):
    return_dic = {}
    keys_li = [key for key in ordered_dic]
    pos = -1
    length = len(ordered_dic)
    while pos < len(ordered_dic):
        pos = pos + 1
        if pos>len(keys_li)-1:
            unit = keys_li[pos-1]
            unit = get_next_key(time_quan,unit)
            if ordered_dic[unit] == 0 and unit != keys_li[-1]: break
            keys_li.append(unit)
        else:
            unit = keys_li[pos]

        num,unit = ordered_dic[unit],unit

        num_up = int(float(num)/time_quan[unit])
        num_ = float(num) - num_up*time_quan[unit]
        unit_up = get_next_key(time_quan,unit)
        ordered_dic[unit] = int(num_)
            
        if unit_up in ordered_dic:
            ordered_dic[unit_up] = num_up + ordered_dic[unit_up]
        elif unit_up in time_quan:
            ordered_dic[unit_up] = num_up
        elif unit_up == False:
            unit_up = num_up
            ordered_dic[unit] = num_up
        
    return ordered_dic

def remove_zero(dic):
    keys = [key for key in dic]
    pos = -1
    while(pos<len(keys)-1):
        pos = pos + 1
        
        key = keys[pos]
        value = dic[key]
        
        if value == 0:
            del keys[pos]
            del dic[key]
            pos = pos - 1

    return dic
    
def reverse_dic(dic):
    rev_li = []
    for c in dic.keys():
        rev_li = [c] + rev_li
    
    rev_dic = {}
    for c in rev_li:
        rev_dic[c] = dic[c]
    return rev_dic

def time_dic2str(dic):
    return ''.join([str(dic[key])+key for key in dic])

def simplify_time(time_str):
    time_dic = str2time_dic(time_str)
    ordered_dic = reverse_dic(time_dic)
    return time_dic2str(reverse_dic(remove_zero(shorten_time(ordered_dic))))

def calculate_deficit_or_excess_sleep(bedtime,gateuptime,reqtime):
    bedtime_obj = datetime.strptime(bedtime, '%d/%m/%y %I:%M%p')
    gateuptime_obj = datetime.strptime(gateuptime, '%d/%m/%y %I:%M%p')
    reqtime_obj = datetime.strptime(reqtime, '%I:%M:%S')
    slept_time_delta = gateuptime_obj - bedtime_obj
    reqtime_delta = timedelta(hours=reqtime_obj.hour, minutes=reqtime_obj.minute, seconds=reqtime_obj.second)
    deficit_seconds = (slept_time_delta - reqtime_delta).total_seconds()
    simplified_deficit_time = simplify_time(str(deficit_seconds)+"seconds")
    return simplified_deficit_time


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.Entry_Args = args
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox(self.Entry_Args[0])
                    self.lb.config(width=0)
                    """
                    scrollbar = Scrollbar(self.Entry_Args[0])
                    self.lb.config(yscrollcommand=scrollbar.set)
                    lis = self.lb
                    scrollbar.config(command=lis.yview)
                    scrollbar.pack(side=RIGHT, fill=Y)
                    """
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

