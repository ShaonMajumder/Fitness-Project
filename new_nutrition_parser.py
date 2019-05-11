from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.common.exceptions import NoAlertPresentException,TimeoutException,NoSuchElementException,WebDriverException,ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Pool
from bs4 import BeautifulSoup

import time
import sys
import logging
import configparser
import codecs
import re
import os
import chardet
import requests
import json
import platform

def filter_value(value):
	if ' grams' in value:
		value = value.replace(' grams','')
	elif ' g' in value:
		value = value.replace(' g','')
	elif ' mg' in value:
		value = value.replace(' mg','')
		value = str(float(value)/1000)
	return value

def parse_nutrition(string):
	driver = webdriver.Chrome('driver/chromedriver.exe')
	driver.set_window_size(1920, 1040)
	driver.get('https://www.google.com/search?q='+string+'+nutrition+value')
	wiki_ = driver.find_element_by_xpath('//div[@class="SALvLe farUxc mJ2Mod"]')

	nutritients = {}
	nutritients['Name'] = string
	#Macro Nutrients
	res_key = ['Amount Per','Calories','Total Fat','Cholesterol','Sodium','Potassium','Total Carbohydrate','Protein','Caffeine']
	for element in driver.find_elements_by_xpath('//span[@class="V6Ytv"]'):
		key = element.get_attribute("innerHTML")
		if key in res_key:
			if key == 'Amount Per':
				value = element.find_element_by_xpath('following-sibling::select').get_attribute("title")
			else:
				value = element.find_element_by_xpath('following-sibling::span[@class="abs"]').get_attribute("innerHTML")
			if value != '': nutritients[key] = value

	#Sub Nutrients
	sub_res_key = ['Saturated fat','Polyunsaturated fat','Monounsaturated fat','Dietary fiber','Sugar']
	for element in driver.find_elements_by_xpath('//td[@class="ellip VDcZVe"]'):
		key_ = element.find_element_by_xpath('span')
		key = key_.get_attribute("innerHTML")
		if key in sub_res_key:
			value = key_.find_element_by_xpath('following-sibling::span[@class="abs"]').get_attribute("innerHTML")
			nutritients[key] = value

	#Other Micronutrient than Sodium,Potassium
	for element in wiki_.find_elements_by_xpath('//td[@class="ellip" and @role="listitem"]'):
		key = element.get_attribute("innerHTML")
		value = element.find_element_by_xpath('following-sibling::td[contains(@class,"ellip fooDZe")]/span[@class="pdv"]').get_attribute("innerHTML")
		nutritients[key] = value

	_ = {}
	for key in nutritients:
		key_ = key.replace('-','')
		key_ = key_.replace(' ','_')
		if key_ in ['Amount_Per','Total_Fat','Total_Carbohydrate','Protein','Saturated_fat','Polyunsaturated_fat','Monounsaturated_fat','Trans_Fat','Cholesterol','Dietary_fiber','Sugar','Sodium','Potassium']:
			key_ = key_+'_grams'
			value = filter_value(nutritients[key])
		else:
			value = nutritients[key]
		_[key_] = value
	nutritients = _
	
	"""
	Calories = {Calories}
	Total Fat = {Total_Fat}
		Saturated Fat = {Saturated_Fat}
		Polyunsaturated Fat = {Polyunsaturated_Fat}
		Monounsaturated Fat = {Monounsaturated_Fat}
	Cholesterol = {Cholesterol}
	Sodium = {Sodium}
	Potassium = {Potassium}
	Total_Carbohydrate = {Total_Carbohydrate}
		Dietary Fiber = {Dietary_Fiber}
		Sugar = {Sugar}
	Protein = {Protein}
	"""
	driver.quit()
	return nutritients

from utilities.gsheet import *
from utilities.utility import *
utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
cred_json_file = utilization_directory+'sheet_credentials.json'


google_sheet_client_id = config['GOOGLE_SHEET']['google_sheet_client_id']
google_sheet_client_secret = config['GOOGLE_SHEET']['google_sheet_client_secret']

SPREADSHEET_ID = config['GOOGLE_SHEET']['spreadsheet_id']
google_sheet_range = config['GOOGLE_SHEET']['spreadsheet_range']
gsheet = Gsheet(cred_json_file,SPREADSHEET_ID)

new_row = len(gsheet.get_values('Sheet1'))+1
nutrients = parse_nutrition('rice')
nutrients['id'] = new_row - 1
for nut in nutrients:
	sheet_name = 'Sheet1'
	range_letter = gsheet.get_rangename_from_column_name(SPREADSHEET_ID,'Sheet1',nut)
	update_cell_range = sheet_name+"!"+range_letter+str(new_row)
	update_area_range = update_cell_range #AG44'
	gsheet.update_cell(update_area_range,update_cell_range,nutrients[nut])


