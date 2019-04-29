import pymysql
import pandas as pd

"""
Examples :
#mydb.insert(['title','resource_url'],['v1','v2'],'data')
#result = mydb.select(['name', 'value', 'id'],"`name` = 'mean_required_sleep_time'","constants")
#mydb.edit(['name','value'],['n1','v1'],"`id` = 5","constants")
#mydb.import_from_xlsx('safe_directory/nutrition_values.xlsx','nutrition_values')
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
    
    def create_table(self,column_names,database):
        stri = " VARCHAR(100), ".join(column_names) + " VARCHAR(100)"
        query = "CREATE TABLE "+database+ " ( "+stri+" )"
        return self.execute(query)

    def import_from_xlsx(self,xlsx_filename,database):
        db = pd.read_excel(xlsx_filename, encoding='utf-8')
        rows = db.shape[0]
        columns = list(db.columns)
        self.create_table(columns,database)
        data2d = []
        for row in db.iterrows():
            index, data = row
            data2d.append(data.tolist())

        for row_li in data2d:
            self.insert(columns,row_li,database)


    def insert(self,keys,values,database):
        key_str = '`' + '`,`'.join(keys) + '`'
        value_str = "'" + "','".join(str(v) for v in values) + "'"
        
        query = "INSERT INTO `"+database+"` ("+key_str+") VALUES ("+value_str+")"
        return self.execute(query)

    def select(self,keys,condition_str,database):
        if keys == '*':
            key_str = '*'
        else:
            key_str = '`' + '`,`'.join(keys) + '`'
        if condition_str == "":
            condition_str = "True"

        query = "SELECT "+key_str+" FROM `"+database+"` where "+condition_str
        return self.execute(query)

    def edit(self,keys,values,condition,database):
        key_val_str = ""
        for key,value in zip(keys,values):
            key_val_str = key_val_str + "`"+key+"` = '"+value+"',"
        
        key_val_str = key_val_str[:-1]
        query = "UPDATE `"+database+"` SET "+key_val_str+" where "+condition
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
