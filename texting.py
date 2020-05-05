import MySQLdb
from datetime import datetime, timedelta
import os

db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()
a=[]
sql="SELECT a.booking_time, b.service_name FROM timetable a, service b WHERE a.service=b.service_ID and a.remark IS NULL"
cursor.execute(sql)
service_total_nonremark=cursor.fetchall()
for i in service_total_nonremark:
    a.append(i)
print(a)

