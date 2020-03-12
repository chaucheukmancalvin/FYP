import MySQLdb
from datetime import datetime, timedelta
import os

db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()

sql="ALTER TABLE seat CHANGE available seat_condition varchar(50)"
cursor.execute(sql)
db.commit()
print("DONE")

