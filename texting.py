import MySQLdb
from datetime import datetime, timedelta
import os

db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()

sql="SELECT password FROM member WHERE member_ID='M0000001'"
cursor.execute(sql)
password=cursor.fetchone()
print(password)

