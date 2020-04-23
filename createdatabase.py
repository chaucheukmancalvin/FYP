import MySQLdb
db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()

sql48="ALTER TABLE staff_holiday DROP FOREIGN KEY FK_staff_holiday_staff"
cursor.execute(sql48)

sql37="ALTER TABLE service DROP FOREIGN KEY FK_category"
cursor.execute(sql37)

sql38="ALTER TABLE member DROP FOREIGN KEY FK_membership"
cursor.execute(sql38)

sql39="ALTER TABLE timetable DROP FOREIGN KEY FK_timetable_service"
cursor.execute(sql39)

sql40="ALTER TABLE timetable DROP FOREIGN KEY FK_timetable_staff"
cursor.execute(sql40)

sql41="ALTER TABLE timetable DROP FOREIGN KEY FK_timetable_seat"
cursor.execute(sql41)

sql42="ALTER TABLE timetable DROP FOREIGN KEY FK_timetable_member"
cursor.execute(sql42)

sql43="ALTER TABLE score DROP FOREIGN KEY FK_score_service"
cursor.execute(sql43)

sql44="ALTER TABLE score DROP FOREIGN KEY FK_score_staff"
cursor.execute(sql44)

sql49="ALTER TABLE working_week DROP FOREIGN KEY FK_working_week_staff"
cursor.execute(sql49)

sql58="ALTER TABLE product_usage DROP FOREIGN KEY FK_product_usage"
cursor.execute(sql58)

sql59="ALTER TABLE product_usage DROP FOREIGN KEY FK_service_usage"
cursor.execute(sql59)

sql60="ALTER TABLE stock DROP FOREIGN KEY FK_stock"
cursor.execute(sql60)

sql66="ALTER TABLE remark DROP FOREIGN KEY FK_remark"
cursor.execute(sql66)

#----------

sql67="DROP TABLE remark"
cursor.execute(sql67)

sql61="DROP TABLE product_usage"
cursor.execute(sql61)

sql28="DROP TABLE staff"
cursor.execute(sql28)

sql29="DROP TABLE staff_holiday"
cursor.execute(sql29)

sql30="DROP TABLE category"
cursor.execute(sql30)

sql31="DROP TABLE service"
cursor.execute(sql31)

sql32="DROP TABLE seat"
cursor.execute(sql32)

sql33="DROP TABLE membership"
cursor.execute(sql33)

sql34="DROP TABLE member"
cursor.execute(sql34)

sql35="DROP TABLE timetable"
cursor.execute(sql35)

sql36="DROP TABLE score"
cursor.execute(sql36)

sql50="DROP TABLE working_week"
cursor.execute(sql50)

sql62="DROP TABLE stock"
cursor.execute(sql62)

sql63="DROP TABLE product"
cursor.execute(sql63)

#--------------------------------------------------
sql="CREATE TABLE staff (staff_ID CHAR(8) PRIMARY KEY NOT NULL, staff_name VARCHAR(50) NOT NULL, gender CHAR(1) NOT NULL, position VARCHAR(20) NOT NULL, salary FLOAT(1) NOT NULL, price FLOAT(1) NOT NULL, working_hour TIME(0) NOT NULL)"
cursor.execute(sql)

sql0="CREATE TABLE staff_holiday (staff CHAR(8) NOT NULL, holiday DATETIME NOT NULL, holiday_duration TIME(0) NOT NULL)"
cursor.execute(sql0)

sql1="CREATE TABLE category (category_ID CHAR(2) PRIMARY KEY NOT NULL, category_name VARCHAR(50) NOT NULL)"
cursor.execute(sql1)

sql2="CREATE TABLE service (service_ID CHAR(3) PRIMARY KEY NOT NULL, service_name VARCHAR(50) NOT NULL, category CHAR(2) NOT NULL,price FLOAT(1) NOT NULL, duration TIME(0))"
cursor.execute(sql2)

sql3="CREATE TABLE seat (seat_ID CHAR(2) PRIMARY KEY NOT NULL, available CHAR(1) NOT NULL)"
cursor.execute(sql3)

sql4="CREATE TABLE membership (membership_ID CHAR(1) PRIMARY KEY NOT NULL, discount FLOAT(2) NOT NULL)"
cursor.execute(sql4)

sql5="CREATE TABLE member (member_ID CHAR(8) PRIMARY KEY NOT NULL, member_name VARCHAR (50) NOT NULL, password VARCHAR(20) NOT NULL, membership CHAR(1) NOT NULL)"
cursor.execute(sql5)

sql6="CREATE TABLE timetable (service CHAR(3) NOT NULL, staff CHAR(8) NOT NULL, booking_time DATETIME NOT NULL, seat CHAR(2) NOT NULL, member CHAR(8), score FLOAT(1))"
cursor.execute(sql6)

sql7="CREATE TABLE score (service CHAR(3) NOT NULL, staff CHAR(8) NOT NULL, score FLOAT(1))"
cursor.execute(sql7)

sql45="CREATE TABLE working_week (week CHAR(3) NOT NULL, staff CHAR(8) NOT NULL)"
cursor.execute(sql45)

sql51="CREATE TABLE product(product_ID CHAR(2) PRIMARY KEY NOT NULL, product_name VARCHAR(50) NOT NULL, price FLOAT(1) NOT NULL, capacity_ml INT(5) NOT NULL)"
cursor.execute(sql51)

sql52="CREATE TABLE stock(product CHAR(2) PRIMARY KEY NOT NULL, product_number INT(5) NOT NULL)"
cursor.execute(sql52)

sql53="CREATE TABLE product_usage(product CHAR(2) NOT NULL, service CHAR(3) NOT NULL, estimate_usage FLOAT(2) NOT NULL)"
cursor.execute(sql53)

sql64="CREATE TABLE remark (reamrk_ID CHAR(3) PRIMARY KEY NOT NULL, service CHAR(3) NOT NULL, remark_name VARCHAR(50) NOT NULL, price FLOAT(1) NOT NULL)"
cursor.execute(sql64)

#------------------------------------------------
sql8="ALTER TABLE staff_holiday ADD PRIMARY KEY (staff,holiday)"
cursor.execute(sql8)

sql9="ALTER TABLE staff_holiday ADD CONSTRAINT FK_staff_holiday_staff FOREIGN KEY (staff) REFERENCES staff(staff_ID)"
cursor.execute(sql9)

sql10="ALTER TABLE service ADD CONSTRAINT FK_category FOREIGN KEY (category) REFERENCES category(category_ID)"
cursor.execute(sql10)

sql11="ALTER TABLE member ADD CONSTRAINT FK_Membership FOREIGN KEY (membership) REFERENCES membership(membership_ID)"
cursor.execute(sql11)

sql12="ALTER TABLE timetable ADD PRIMARY KEY (staff,booking_time,seat)"
cursor.execute(sql12)

sql13="ALTER TABLE timetable ADD CONSTRAINT FK_timetable_service FOREIGN KEY (service) REFERENCES service(service_ID)"
cursor.execute(sql13)

sql14="ALTER TABLE timetable ADD CONSTRAINT FK_timetable_staff FOREIGN KEY (staff) REFERENCES staff(staff_ID)"
cursor.execute(sql14)

sql15="ALTER TABLE timetable ADD CONSTRAINT FK_timetable_seat FOREIGN KEY (seat) REFERENCES seat(seat_ID)"
cursor.execute(sql15)

sql16="ALTER TABLE timetable ADD CONSTRAINT FK_timetable_member FOREIGN KEY (member) REFERENCES member(member_ID)"
cursor.execute(sql16)

sql17="ALTER TABLE score ADD PRIMARY KEY (service, staff)"
cursor.execute(sql17)

sql18="ALTER TABLE score ADD CONSTRAINT FK_score_service FOREIGN KEY (service) REFERENCES service(service_ID)"
cursor.execute(sql18)

sql19="ALTER TABLE score ADD CONSTRAINT FK_score_staff FOREIGN KEY (staff) REFERENCES staff(staff_ID)"
cursor.execute(sql19)

sql46="ALTER TABLE working_week ADD PRIMARY KEY (week, staff)"
cursor.execute(sql46)

sql47="ALTER TABLE working_week ADD CONSTRAINT FK_working_week_staff FOREIGN KEY (staff) REFERENCES staff(staff_ID)"
cursor.execute(sql47)

sql54="ALTER TABLE stock ADD CONSTRAINT FK_stock FOREIGN KEY (product) REFERENCES product(product_ID)"
cursor.execute(sql54)

sql55="ALTER TABLE product_usage ADD PRIMARY KEY (product,service)"
cursor.execute(sql55)

sql56="ALTER TABLE product_usage ADD CONSTRAINT FK_product_usage FOREIGN KEY (product) REFERENCES product(product_ID)"
cursor.execute(sql56)

sql57="ALTER TABLE product_usage ADD CONSTRAINT FK_service_usage FOREIGN KEY (service) REFERENCES service(service_ID)"
cursor.execute(sql57)

sql65="ALTER TABLE remark ADD CONSTRAINT FK_remark FOREIGN KEY (service) REFERENCES service(service_ID)"
cursor.execute(sql65)

#--------------------------------------------
sql20="INSERT INTO staff (staff_ID, staff_name, gender, position, salary, price, working_hour) VALUES (%s , %s, %s, %s, %s, %s, %s)"
val=("S0000001","Calvin", "M", "Admin", 10000.0, 30.0, "08:00:00")
cursor.execute(sql20,val)
db.commit()

sql21="INSERT INTO category (category_ID, category_name) VALUES (%s ,%s)"
val0=("C1","hair service")
cursor.execute(sql21,val0)
db.commit()

sql22="INSERT INTO service (service_ID, service_name, category, price, duration) VALUES (%s ,%s, %s, %s, %s)"
val1=("001","hair Cut", "C1", 120.0, "1:00:00", "S0000001")
cursor.execute(sql22,val1)
db.commit()

sql23="INSERT INTO seat (seat_ID, available) VALUES (%s ,%s)"
val2=("S1","Y")
cursor.execute(sql23,val2)
db.commit()

sql24="INSERT INTO membership (membership_ID, discount) VALUES (%s ,%s)"
val3=("1",0.95)
cursor.execute(sql24,val3)
db.commit()

sql25="INSERT INTO member (member_ID, member_name, password ,membership) VALUES (%s, %s, %s, %s)"
val4=("M0000001","Calvin","password","1")
cursor.execute(sql25,val4)
db.commit()

sql26="INSERT INTO timetable (service, staff, booking_time, seat) VALUES (%s ,%s, %s, %s)"
val5=("001","S0000001", "2020-01-01 00:00:00", "S1")
cursor.execute(sql26,val5)
db.commit()

sql27="INSERT INTO score (service, staff) VALUES (%s ,%s)"
val6=("001","S0000001")
cursor.execute(sql27,val6)
db.commit()

#cursor.execute("SELECT * FROM staff")
#result = cursor.fetchall()
#for x in result:
#  print(x)
print('done')