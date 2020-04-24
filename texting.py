import MySQLdb
from datetime import datetime, timedelta
import os

db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()

sql="SELECT a.service_name, b.staff_name, c.booking_time, c.seat, c.score, c.remark FROM service a, staff b, timetable c WHERE a.service_ID=c.service and b.staff_ID=c.staff and c.member='M0000001' "
cursor.execute(sql)
table=cursor.fetchall()
Table=list(table)
for n,i in enumerate(Table):
    if i[5]!=None:
        sql="SELECT a.service_name, b.staff_name, c.booking_time, c.seat, c.score, d.remark_name FROM service a, staff b, timetable c, remark d WHERE a.service_ID=c.service and b.staff_ID=c.staff and c.member='M0000001' and d.remark_ID=c.remark and c.booking_time='%s'"%i[2]
        cursor.execute(sql)
        new=cursor.fetchone()
        Table[n]=new
print(Table[0])
    


