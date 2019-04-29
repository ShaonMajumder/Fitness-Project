import pymysql

"""
Examples :
#mydb.insert(['title','resource_url'],['v1','v2'],'data')
#result = mydb.select(['name', 'value', 'id'],"`name` = 'mean_required_sleep_time'","constants")
#mydb.edit(['name','value'],['n1','v1'],"`id` = 5","constants")
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
