import MySQLdb
from datetime import datetime, timedelta
import os

db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()




