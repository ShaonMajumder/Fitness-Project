from __future__ import print_function
from pprint import pprint
from googleapiclient import discovery
from utility import *

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

"""
utilization_directory = '../safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")
cred_json_file = utilization_directory+'sheet_credentials.json'
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config['GOOGLE_SHEET']['spreadsheet_id']
FINDAREA_RANGE_NAME = config['GOOGLE_SHEET']['spreadsheet_range']
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def colnum_string(num,res=''):
	return colnum_string((num - 1) // 26, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[(num - 1) % 26] + res) if num > 0 else res

class Gsheet:
	"""docstring for Gsheet"""
	def __init__(self, cred_json_file, SPREADSHEET_ID):
		creds = self.get_credential(cred_json_file)
		service = build('sheets', 'v4', credentials=creds)
		sheet = service.spreadsheets()
		self.sheet = sheet
		self.SPREADSHEET_ID = SPREADSHEET_ID

	def get_credential(self,cred_json_file):
		creds = None
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists('token.pickle'):
		    with open('token.pickle', 'rb') as token:
		        creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
		    if creds and creds.expired and creds.refresh_token:
		        creds.refresh(Request())
		    else:
		        flow = InstalledAppFlow.from_client_secrets_file(cred_json_file, SCOPES)
		        creds = flow.run_local_server()
		    # Save the credentials for the next run
		    with open('token.pickle', 'wb') as token:
		        pickle.dump(creds, token)

		return creds
	def get_values(self,FINDAREA_RANGE_NAME):
		result = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
	                            range=FINDAREA_RANGE_NAME).execute()
		values = result.get('values', [])
		return values

	def get_rangename_from_column_name(self,SPREADSHEET_ID,FINDAREA_RANGE_NAME,colnum_name):
		values = self.get_values(FINDAREA_RANGE_NAME)
		row_num = values[0].index(colnum_name)
		return colnum_string(row_num+1)

	def update_cell(self,update_area_range,update_cell_range,update_value):
		# How the input data should be interpreted.

		# TODO: Change placeholder below to generate authentication credentials. See
		# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
		#
		# Authorize using one of the following scopes:
		#     'https://www.googleapis.com/auth/drive'
		#     'https://www.googleapis.com/auth/drive.file'
		#     'https://www.googleapis.com/auth/spreadsheets'

		# The A1 notation of the values to update.

		value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.
		value_range_body = {
		    # TODO: Add desired entries to the request body. All existing entries
		    # will be replaced.
		    'range': update_cell_range,
		    'values': [
		        [update_value]
		    ]
		}

		request = self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range=update_area_range, valueInputOption=value_input_option, body=value_range_body)
		response = request.execute()

		# TODO: Change code below to process the `response` dict:
		pprint(response)
		return response
"""
def main():
	gsheet = Gsheet(cred_json_file)
	
	
	range_num = "44"
	range_letter = range_letter = gsheet.get_rangename_from_column_name(SPREADSHEET_ID,'Sheet1','Food_Id')
	update_cell_range = "Sheet1!"+range_letter+range_num
	update_area_range = update_cell_range
	gsheet.update_cell(update_area_range,update_cell_range,'success2')
	#length_cell = len
	#print([c for c in range(1,length_cell+1)])
if __name__ == '__main__':
    main()
"""