from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout,ReadTimeout,ConnectionError
from tkinter import messagebox
from utility import *
import os,re,requests,time,random,codecs,json,chardet,winsound,shutil,configparser
import tkinter
import datetime
import string

datetime_ = datetime.datetime.now().strftime("%d/%m/%y %I:%M%p")
#print(datetime)

config = configparser.ConfigParser()
config.readfp(codecs.open("config.ini", "r", "utf8"))

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

query = "SELECT * FROM sleep_data WHERE `id` != 1 ORDER BY id DESC LIMIT 1"
result = mydb.execute(query)[0]

if result['bed_time'] != '0000-00-00 00:00:00':
	print(result['bed_time'])
else:
	print(datetime.datetime.now())


overall_sleep_excess_or_deficit_time = result['overall_sleep_excess_or_deficit_time'] #from database #initially 0, can be +/- type float
min_required_sleep_time = result['min_required_sleep_time']

time_units = ['years','months','days','hours','minutes','seconds']
time_quan = {'seconds':60, 'minutes':60, 'hours':24, 'days':30, 'months':12, 'years':1}

def get_previous_key(d,target_key):
	pos = -1
	for key in d:
	    pos=pos+1
	    if key == target_key:
	        listForm = list(d.keys())
	        if (pos-1)< len(d):
	        	return listForm[pos-1]
	        else:
	        	return False



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
		dic[unit] = int(num)

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

		
"""
print(simplify_time('90seconds'))
print(simplify_time('8hours61minutes90seconds'))
print(simplify_time('120years10months15days8hours60minutes90seconds'))
"""
def time_difference(time_start,time_stop):
	time_start,time_stop = simplify_time(time_start),simplify_time(time_stop)
	print(time_stop,time_start)
	return_dic = {}
	rev_time_start = reverse_dic(time_start)
	hate = 0
	for unit in rev_time_start:
		if unit in time_stop:
			time_stop_ = time_stop[unit]
			if hate == 0:
				time_stop_ = time_stop[unit]
			else:
				time_stop_ = time_stop[unit] - 1
				hate = 0
			time_start_ = rev_time_start[unit]
			_ = time_stop_ - time_start_
			if _ < 0:
				dhar = time_quan[get_previous_key(time_quan, unit)]
				time_stop_ = time_stop_ + dhar
				_ = time_stop_ - time_start_
				hate = 1
			return_dic[unit] = _

	return return_dic

#print(time_difference("9hours39minutes","12hours69minutes"))
#print(time_difference("2days9hours39minutes","12hours69minutes"))

from datetime import datetime,timedelta
bed_object = datetime.strptime('16/04/19 11:00PM', '%d/%m/%y %I:%M%p')
awake_object = datetime.strptime('17/04/19 6:00AM', '%d/%m/%y %I:%M%p')
#2019-04-17 06:00:00
print(datetime.strptime('01:00:00', '%I:%M:%S')) #  06:00:00 %H:%M:%S
slept_time = awake_object - bed_object

t = datetime.strptime("08:00:00", '%I:%M:%S')
min_delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
deficit_seconds = (slept_time-min_delta).total_seconds()
deficit = slept_time-min_delta


def delta_time(time_str,format_str):
	time_dic = str2time_dic(time_str)
	print(time_dic)
	return_str = {}
	for p in format_str:
		if p in time_dic:
			time_digit = time_dic[p]
			return_str[p] = time_digit
		else:
			return_str[p] = 0

	return return_str


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
	if type(time_str) != str:
		time_str = str(time_str)
	digit_n = num - len(time_str)
	num_ = ""
	for c in range(digit_n):
		num_ = num_ + "0"
	num_ = num_+time_str
	return num_


#print(simplify_time(str(deficit_seconds)+"seconds"))
#print(simplify_time("12000000seconds"))
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


#print(delta_time(time_str,['hours','minutes','seconds']))

print(datetime.strptime('2019-04-16 23:00:00', '%d/%m/%y %I:%M%p'))

exit()
"""
save in database
bed_time
wakeup_time 
todays_slept_time
todays_deficit_or_excess_sleep_time
overall_sleep_excess_or_deficit_time
"""
bed_time = 0
wakeup_time = 0
min_required_sleep_time = 0
todays_slept_time = bed_time - wakeup_time
todays_deficit_or_excess_sleep_time = todays_slept_time - min_required_sleep_time
overall_sleep_excess_or_deficit_time = todays_deficit_or_excess_sleep_time + overall_sleep_excess_or_deficit_time

