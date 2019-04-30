from __future__ import print_function
import pymysql
import pandas as pd


import pickle
import os.path

import pandas as pd





"""
Examples :
#mydb.insert(['title','resource_url'],['v1','v2'],'data')
#result = mydb.select(['name', 'value', 'id'],"`name` = 'mean_required_sleep_time'","constants")
#mydb.edit(['name','value'],['n1','v1'],"`id` = 5","constants")
#mydb.import_from_xlsx('safe_directory/nutrition_values.xlsx','nutrition_values')
#mydb.delete_table('nutrition_values')
#mydb.help()
#columns = mydb.get_columns('workout_moves_data')
"""

class mysql_db():
    def __init__(self, host, user, password, db, charset, cursorclass):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        if type(cursorclass) == str:
            self.cursorclass = eval(cursorclass)
        else:
            self.cursorclass = cursorclass
    def help(self):
        custom_methods = [dir_name for dir_name in dir(mysql_db) if not '__' in dir_name]
        print("Class Methods -> " + str(custom_methods))
    def get_columns(self,table_name):
        results = self.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '"+self.db+"' AND TABLE_NAME = '"+table_name+"'");
        columns = [result['COLUMN_NAME'] for result in results]
        return columns

    def create_table(self,column_names,table):
        stri = " VARCHAR(100), ".join(column_names) + " VARCHAR(100)"
        query = "CREATE TABLE "+table+ " ( "+stri+" )"
        return self.execute(query)
    def delete_table(self,table):
        #check if exist then drop table
        query = "SHOW TABLES LIKE '"+table+"'"
        result = self.execute(query)
        
        if result == ():
            print("Table "+table+" does not exists")
        else:
            query = "DROP TABLE "+table
            return self.execute(query)


    def import_from_xlsx(self,xlsx_filename,table):
        db = pd.read_excel(xlsx_filename, encoding='utf-8')
        
        columns = list(db.columns)
        self.create_table(columns,table)
        data2d = []
        for row in db.iterrows():
            index, data = row
            data2d.append(data.tolist())

        for row_li in data2d:
            self.insert(columns,row_li,table)


    def insert(self,keys,values,table):
        key_str = '`' + '`,`'.join(keys) + '`'
        value_str = "'" + "','".join(str(v) for v in values) + "'"
        
        query = "INSERT INTO `"+table+"` ("+key_str+") VALUES ("+value_str+")"
        return self.execute(query)

    def select(self,keys,condition_str,table):
        if keys == '*':
            key_str = '*'
        else:
            key_str = '`' + '`,`'.join(keys) + '`'
        if condition_str == "":
            condition_str = "True"

        query = "SELECT "+key_str+" FROM `"+table+"` where "+condition_str
        return self.execute(query)

    def edit(self,keys,values,condition,table):
        key_val_str = ""
        for key,value in zip(keys,values):
            key_val_str = key_val_str + "`"+key+"` = '"+value+"',"
        
        key_val_str = key_val_str[:-1]
        query = "UPDATE `"+table+"` SET "+key_val_str+" where "+condition
        return self.execute(query)

    def execute(self,query):
        # Connect to the database
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset, cursorclass=self.cursorclass)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = query
                cursor.execute(sql)
                results = cursor.fetchall()

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        return results

    def import_list_from_google_sheet(self,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME,db_table):

        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request



        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        """
        google_sheet_client_id = config['GOOGLE_SHEET']['google_sheet_client_id']
        google_sheet_client_secret = config['GOOGLE_SHEET']['google_sheet_client_secret']

        google_sheet_id = config['GOOGLE_SHEET']['spreadsheet_id']
        google_sheet_range = config['GOOGLE_SHEET']['spreadsheet_range']
        """
        

        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
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
                flow = InstalledAppFlow.from_client_secrets_file(
                    'safe_directory/credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            return values
    def import_table_from_google_sheet(self,google_sheet_id,google_sheet_range,db_table):
        values = self.import_list_from_google_sheet(google_sheet_id,google_sheet_range,db_table)
        header = values.pop(0)
        df = pd.DataFrame(values, columns=header)
        df.to_excel("safe_directory/nutrition_values.xlsx")
        self.delete_table(db_table)
        self.import_from_xlsx('safe_directory/nutrition_values.xlsx',db_table)