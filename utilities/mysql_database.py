from __future__ import print_function
try:
    from utilities.gsheet import *
except:
    from gsheet import *

import pymysql
import pandas as pd
import os
import pickle
import os.path
import pandas as pd
import numpy as np

"""
Examples :
#mydb.insert(['title','resource_url'],['v1','v2'],'data')
#result = mydb.select(['name', 'value', 'id'],"`name` = 'mean_required_sleep_time'","constants")
#mydb.edit(['name','value'],['n1','v1'],"`id` = 5","constants")
#mydb.import_from_xlsx('filename.xlsx','nutrition_values')
#mydb.delete_table('nutrition_values')
#mydb.help()
#columns = mydb.get_columns('workout_moves_data')
#mydb.shift_down_one_row_space('id','4','workout_moves_data')
#mydb.shift_up_one_row_space('id','4','workout_moves_data')
#mydb.create_row_space_at('id',4,'workout_moves_data')
#mydb.remove_row_space_at('id',4,'workout_moves_data')
#mydb.rearrange_ids('id','day_exercise_planning')
#mydb.export_column('Food_Id','nutrition_values')
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

    def help(self):
        custom_methods = [dir_name for dir_name in dir(mysql_db) if not '__' in dir_name]
        print("Class Methods -> " + str(custom_methods))

    def select(self,keys,condition_str,table):
        if keys == '*':
            key_str = '*'
        else:
            key_str = '`' + '`,`'.join(keys) + '`'
        if condition_str == "":
            condition_str = "True"

        query = "SELECT "+key_str+" FROM `"+table+"` where "+condition_str
        return self.execute(query)

    def insert(self,keys,values,table):
        key_str = '`' + '`,`'.join(keys) + '`'
        value_str = "'" + "','".join(str(v) for v in values) + "'"
        
        query = "INSERT INTO `"+table+"` ("+key_str+") VALUES ("+value_str+")"
        return self.execute(query)

    def edit(self,keys,values,condition,table):
        key_val_str = ""
        for key,value in zip(keys,values):
            key_val_str = key_val_str + "`"+key+"` = '"+value+"',"
        
        key_val_str = key_val_str[:-1]
        query = "UPDATE `"+table+"` SET "+key_val_str+" where "+condition
        return self.execute(query)

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

    def create_row_space_at(self,primary_key,new_row,db_table):
        #Making space in middle
        after_row = new_row - 1
        self.shift_down_one_row_space(primary_key,after_row,db_table)

    def remove_row_space_at(self,primary_key,blank_row,db_table):
        #Making space in middle
        self.shift_up_one_row_space(primary_key,blank_row,db_table)

    def shift_down_one_row_space(self,primary_key,after_row,db_table):
        query = f"""UPDATE `{db_table}` SET {primary_key} = {primary_key} + 1 WHERE id > {after_row} ORDER BY {primary_key} DESC"""
        self.execute(query)

    def shift_up_one_row_space(self,primary_key,after_row,db_table):
        query = f"""UPDATE `{db_table}` SET {primary_key} = {primary_key} - 1 WHERE id > {after_row} ORDER BY {primary_key} ASC"""
        self.execute(query)

    def reset_autoincrement_from(self,from_,db_table):
        query = f"""ALTER TABLE `{db_table}` AUTO_INCREMENT = {from_}"""
        self.execute(query)

    def rearrange_ids(self,primary_key,db_table):
        #SET @count = 0;
        #UPDATE `table_name` SET `table_name`.`id` = @count:= @count + 1;

        query = f"""UPDATE `{db_table}` cross join (select @count:=0) as init SET `{db_table}`.`{primary_key}`=@count:=@count+1"""
        self.execute(query)
        self.reset_autoincrement_from(1,db_table)

    def import_from_xlsx(self,xlsx_filename,table):
        db = pd.read_excel(xlsx_filename, na_filter=False, encoding='utf-8')
        
        columns = list(db.columns)
        self.create_table(columns,table)
        data2d = []
        for row in db.iterrows():
            index, data = row
            data2d.append(data.tolist())

        for row_li in data2d:
            self.insert(columns,row_li,table)


    def import_table_from_2D_List(self,values,db_table):
        header = values.pop(0)
        df = pd.DataFrame(values, columns=header)
        temp_file = "temp.xlsx"
        df.to_excel(temp_file)
        self.delete_table(db_table)
        self.import_from_xlsx(temp_file,db_table)
        os.remove(temp_file)

    def export_column(self,target,db_table):
        results = self.select([target],"",db_table)
        for row in results:
            print(row[target])

    def remove_temp(self):
        #remove token file which saves google spreadsheet access
        os.remove('token.pickle')