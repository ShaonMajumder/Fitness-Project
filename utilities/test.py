from mysql_database import *
from utility import *

utilization_directory = '../safe_directory/'
config = read_config_ini(utilization_directory+"config.ini")

host=config['DATABASE']['host']
user=config['DATABASE']['user']
password=config['DATABASE']['password']
db=config['DATABASE']['db']
charset=config['DATABASE']['charset']
cursorclass=config['DATABASE']['cursorclass']

mydb = mysql_db(host, user, password, db, charset, cursorclass)

mydb.rearrange_ids('id','day_exercise_planning')
