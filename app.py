from flask import Flask, render_template, url_for, redirect, request, session
import os
import MySQLdb
from datetime import datetime, timedelta
import calendar
from werkzeug import secure_filename
from flask_mail import Mail, Message
import re
db=MySQLdb.connect(host="127.0.0.1",user="root", passwd="",db="fyp",charset="utf8")
cursor=db.cursor()

UPLOAD_FOLDER = os.getcwd() + '/static' + '/img'
ALLOWED_EXTENSTIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SecretKeyHERE!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '205project2019@gmail.com'
app.config['MAIL_PASSWORD'] = '205project'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSTIONS

@app.route("/")
def index():
    sql="SELECT category_name FROM category"
    cursor.execute(sql)
    category=cursor.fetchall()
    details=[]
    for i in category:
        detail={}
        sql2="SELECT a.service_name, b.category_name FROM service a, category b WHERE b.category_ID=a.category and b.category_name='%s'"%i[0]
        cursor.execute(sql2)
        detail.update(cursor.fetchall())
        details.append(detail)
    print(details)
    sql3="SELECT staff_name FROM staff"
    cursor.execute(sql3)
    staff=cursor.fetchall()
    if session.get('member'):
        sql1="SELECT member_name FROM member WHERE member_ID='%s'"%session['member']
        cursor.execute(sql1)
        member=cursor.fetchone()
        print(member)
        sql3="SELECT booking_time FROM timetable WHERE member='%s' and booking_time >='%s' ORDER BY booking_time ASC"%(session['member'], datetime.today())
        cursor.execute(sql3)
        upcome_booking=cursor.fetchone()
        return render_template('index.html',service=category, member=member, servicedetails=details, staff=staff, upcome_booking=upcome_booking)
    return render_template('index.html',service=category, servicedetails=details, staff=staff)

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/advertisement")
def advertisement():
    return render_template('advertisement.html')

@app.route("/Profile")
def Profile():
    member_id = session['member']
    sql="SELECT a.member_ID, a.member_name, b.membership_name FROM member a, membership b WHERE a.membership = b.membership_ID and a.member_ID='%s'"%member_id
    cursor.execute(sql)
    member=cursor.fetchone()
    try:
       img = open('static/img/' + 'profile' +str(member_id)  + '.' + 'png')
       img.close()
       img = 'png'
       return render_template('Profile.html', member=member, img=img)
    except:
        try:
            img = open('static/img/' + 'profile' + str(member_id)  + '.' + 'jpg')
            img.colse()
            img = 'jpg'
            return render_template('Profile.html', member=member, img=img)
        except:
            try:
                img = open('static/img/' + 'profile' +str(member_id)  + '.' + 'jpeg')
                img.colse()
                img = 'jpeg'
                return render_template('Profile.html', member=member, img=img)
            except:
                return render_template('Profile.html', member=member)

@app.route("/changemember_name", methods=['POST'])
def changemember_name():
    member_id = session['member']
    member_new_name = request.form['username']
    sql="UPDATE member SET member_name = '%s' WHERE member_ID = '%s'"%(member_new_name, member_id)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('Profile'))

@app.route("/changemember_password", methods=['POST'])
def changemember_passsword():
    member_id = session['member']
    member_old_password = request.form['old_password']
    member_new_password = request.form['new_password']
    sql="SELECT * FROM member WHERE member_ID = '%s' and password = '%s'"%(member_id, member_old_password)
    cursor.execute(sql)
    member=cursor.fetchone()
    if member != ():
        sql="UPDATE member SET password = '%s' WHERE member_ID = '%s'"%(member_new_password, member_id)
        cursor.execute(sql)
        db.commit()
    return redirect(url_for('Profile'))

@app.route("/changeprofile_img", methods=['POST'])
def changeprofile_img():
    member_id = session['member']
    try:
        img = request.files['image']
        print('3')
        if 'image' not in request.files:
            print('2')
            return redirect(url_for('Profile'))
        elif img and allowed_file(img.filename):
            filename = 'profile'+ str(member_id) + '.' + secure_filename(img.filename).split('.')[-1]
            if os.path.exists('static/img/' + 'profile' +str(member_id)  + '.' + 'png'):
                os.remove('static/img/' + 'profile' + str(member_id)  + '.' + 'png')
            elif os.path.exists('static/img/' + 'profile' +str(member_id)  + '.' + 'jpg'):
                os.remove('static/img/' + 'profile' +str(member_id)  + '.' + 'jpg')
            elif os.path.exists('static/img/' + 'profile' +str(member_id)  + '.' + 'jpeg'):
                os.remove('static/img/' + 'profile' +str(member_id)  + '.' + 'jpeg')
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('Profile'))
    except:
        print('4')
        return redirect(url_for('Profile'))

@app.route("/contactus")
def contactus():
    return render_template('contactus.html')

@app.route("/history")
def history():
    member=session['member']
    sql="SELECT a.service_name, b.staff_name, c.booking_time, c.seat, c.score FROM service a, staff b, timetable c WHERE a.service_ID=c.service and b.staff_ID=c.staff and c.member='%s'"%member
    cursor.execute(sql)
    table=cursor.fetchall()
    today=datetime.today()
    return render_template('history.html', table=table, today=today)

@app.route("/scoring_mark", methods=['POST'])
def scoring_mark():
    staff_name = request.form['staff']
    service_name = request.form['service']
    date = request.form['date']
    mark = request.form['score']
    sql="SELECT a.booking_time, a.score, b.staff_ID, c.service_ID FROM timetable a, staff b, service c WHERE a.staff=b.staff_ID and a.service=c.service_ID and b.staff_name='%s' and c.service_name='%s' and a.booking_time='%s'"%(staff_name,service_name,date)
    cursor.execute(sql)
    service_appointment = cursor.fetchone()
    if service_appointment != None:
        sql="UPDATE timetable SET score='%s' WHERE booking_time = '%s' and staff='%s' and service='%s'"%(mark,date,service_appointment[2],service_appointment[3])
        cursor.execute(sql)
        db.commit()
        sql="SELECT score, service FROM timetable WHERE service='%s' and staff='%s'"%(service_appointment[3],service_appointment[2])
        cursor.execute(sql)
        total_score=cursor.fetchall()
        totalscore = 0
        count = 0
        if total_score != ():
            print(123)
            for i in total_score:
                if i[0] != None:
                    totalscore += i[0]
                    count+=1
        if count != 0:
            adv_score=totalscore/count
        else:
            adv_score=0
        sql="UPDATE score SET score='%s' WHERE service = '%s' and staff = '%s'"%(adv_score ,service_appointment[3], service_appointment[2])
        cursor.execute(sql)
        db.commit()
    return redirect(url_for('history'))

@app.route("/booking")
def booking():
    try:
        success = request.args['success']
        success = session['success']
        return render_template('booking.html', success=success)
    except:
        try:
            seat = request.args['seat']
            seat = session['seat']
            time = session['time']
            date = session['date']
            staff = session['staff']
            service = session['service']
            sql="SELECT price FROM service WHERE service_name='%s'"%service
            cursor.execute(sql)
            service_price=cursor.fetchone()
            sql1="SELECT price FROM staff WHERE staff_name='%s'"%staff
            cursor.execute(sql1)
            staff_price=cursor.fetchone()
            if session.get('member'):
                sql2 = "SELECT a.discount, b.member_ID FROM membership a, member b WHERE b.member_ID='%s' and b.membership=a.membership_ID"%session['member']
                cursor.execute(sql2)
                discount = cursor.fetchone()
                price = (service_price[0] + staff_price[0]) * discount[0]
            else:
                price = service_price[0] + staff_price[0]
            return render_template('booking.html',service=service, staff=staff, date=date, time=time, seat=seat, price=price)
        except:
            try:
                time = request.args['time']
                time = session['time']
                date = session['date']
                staff = session['staff']
                service = session['service']
                dates = datetime.strptime(date+' '+time ,"%Y-%m-%d %H:%M:%S")
                sql="SELECT duration FROM service WHERE service_name = '%s'"%service
                cursor.execute(sql)
                service_time=cursor.fetchone()
                sql1="SELECT seat_ID FROM seat"
                cursor.execute(sql1)
                seats=cursor.fetchall()
                seat=[]
                for i in seats:    
                    sql2="SELECT a.seat, a.booking_time, b.duration FROM timetable a, service b WHERE b.service_ID=a.service and a.booking_time LIKE '%s%%' and a.seat='%s'"%(str(datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')),i[0])
                    cursor.execute(sql2)
                    busy_seat=cursor.fetchall()
                    print(busy_seat)
                    if busy_seat == ():
                        seat.append(i[0])
                    else:
                        for j in busy_seat:
                            if j[1] <= dates < j[2]+j[1]:
                                print('1')
                            elif j[1] < dates +service_time[0] <= j[2]+j[1]:
                                print('2')
                            elif dates < j[1]:
                                if dates+ service_time[0] > j[2]+j[1]:
                                    print('3')
                                else:
                                    seat.append(j[0])
                            else:
                                seat.append(j[0])
                if session.get('message'):
                    message = request.args['message']
                    message=session['message']
                    session.pop('message',None)
                    return render_template('booking.html',service=service, staff=staff, date=date, time=time, seat=seat, message=message)
                return render_template('booking.html',service=service, staff=staff, date=date, time=time, seat=seat)
            except:
                try:
                    date = request.args['date']
                    date = session['date']
                    staff = session['staff']
                    service = session['service']
                    hour=[]
                    minute=[0,15,30,45]
                    week= int(datetime.strptime(date,'%Y-%m-%d').weekday())
                    if week==5 or week==6:
                        for i in range(11,20):
                            hour.append(i)
                    else:
                        for i in range(9,18):
                            hour.append(i)
                    if session.get('message'):
                        message = request.args['message']
                        message=session['message']
                        session.pop('message',None)
                        return render_template('booking.html',service=service, staff=staff, date=date, hour=hour, minute=minute,message=message)
                    return render_template('booking.html',service=service, staff=staff, date=date, hour=hour, minute=minute)
                except:
                    try:
                        staff = request.args['staff']
                        staff = session['staff']
                        service = session['service']
                        years=int(datetime.today().strftime('%Y'))
                        year=[]
                        month=[]
                        day=[]
                        for i in range(years,2100):
                            year.append(i)
                        for i in range(1,13):
                            month.append(i)
                        for i in range(1,32):
                            day.append(i)
                        if session.get('message'):
                            message = request.args['message']
                            message=session['message']
                            session.pop('message',None)
                            return render_template('booking.html',service=service, staff=staff, year=year, month=month, day=day, message=message)
                        return render_template('booking.html',service=service, staff=staff, year=year, month=month, day=day)
                    except:
                        try:
                            service = request.args['service']
                            service = session['service']
                            sql="SELECT a.staff_name, c.service_name, b.score FROM staff a, score b, service c WHERE a.staff_ID = b.staff and c.service_ID = b.service and c.service_name='%s' ORDER BY b.score DESC"%service
                            cursor.execute(sql)
                            staff_score=cursor.fetchall()
                            sql1="SELECT a.staff_name, c.service_name, a.price FROM staff a, score b, service c WHERE a.staff_ID = b.staff and c.service_ID = b.service and c.service_name='%s' ORDER BY a.price ASC"%service
                            cursor.execute(sql1)
                            staff_price=cursor.fetchall()
                            sql2="SELECT a.staff_name, COUNT(b.service) as exp FROM staff a, (SELECT a.service as service, a.staff as staff FROM timetable a, service b WHERE a.service=b.service_ID and b.service_name='%s') b WHERE a.staff_ID = b.staff GROUP BY a.staff_name ORDER BY exp DESC"%service
                            cursor.execute(sql2)
                            staff_exp=cursor.fetchall()
                            print(staff_exp)
                            if session.get('message'):
                                message = request.args['message']
                                message=session['message']
                                session.pop('message',None)
                                return render_template('booking.html',service=service, staff_score=staff_score, staff_price=staff_price, staff_exp=staff_exp, message=message)
                            return render_template('booking.html',service=service, staff_score=staff_score, staff_price=staff_price, staff_exp=staff_exp)
                        except:
                            if session.get('success'):
                                session.pop('success',None)
                            if session.get('service'):
                                session.pop('service',None)
                            if session.get('staff'):
                                session.pop('staff',None)
                            if session.get('date'):
                                session.pop('date',None)
                            if session.get('time'):
                                session.pop('time',None)
                            if session.get('seat'):
                                session.pop('seat',None)
                            service_sql="SELECT service_name ,duration FROM service ORDER BY duration ASC"
                            cursor.execute(service_sql)
                            service_duration=cursor.fetchall()
                            service_sql1="SELECT service_name ,price FROM service ORDER BY price ASC"
                            cursor.execute(service_sql1)
                            service_price=cursor.fetchall()
                            if session.get('message'):
                                message = request.args['message']
                                message=session['message']
                                session.pop('message',None)
                                return render_template('booking.html',service_duration=service_duration, service_price=service_price, message=message)
                            return render_template('booking.html',service_duration=service_duration, service_price=service_price)

@app.route("/login")
def login():
    try:
        messages = request.args['messages']
        messages = session['messages']
        return render_template('login.html',messages=messages)
    except:
        session.pop('messages',None)
        return render_template('login.html')

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('member',None)
    return redirect(url_for('index'))

@app.route("/loginFunction", methods=['POST'])
def loginFunction():
    userid = request.form['userid']
    password = request.form['password']
    sql="SELECT * FROM member WHERE member_id=%s and password=%s"
    cursor.execute(sql,(userid,password))
    result=cursor.fetchone()
    if result == None:
        sql1="SELECT * FROM staff WHERE staff_id=%s and staff_name=%s"
        cursor.execute(sql1,(userid,password))
        result1=cursor.fetchone()
        if userid == 'admin' and password == 'admin':
            session['admin'] = 'admin'
            return redirect(url_for('admin'))
        elif result1 != None:
            session['staffs'] = result1[0]
            return redirect(url_for('staff'))
        messages = {"main":"*user_id or password fail please try again"}
        session['messages'] = messages
        return redirect(url_for('login', messages=messages))
    else:
        session['member']= userid
        return redirect(url_for('index'))

@app.route("/forgetpassword", methods=['POST'])
def forgetpassword():
    user_ID=request.form['userid']
    username=request.form['username']
    email=request.form['email']
    if re.match("[^@]+@[^@]+\.[^@]+", email):
        sql="SELECT password FROM member WHERE member_ID='%s' and member_name='%s'"%(user_ID,username)
        cursor.execute(sql)
        password=cursor.fetchone()
        if password != None:
            msg = Message('Forgetpassword from salon.',sender='205project2019@gmail.com',recipients=[str(email)])
            msg.body = "Your password is" + " " + str(password[0])
            mail.send(msg)
            messages = {"main":"*email sended"}
            session['messages'] = messages
            return redirect(url_for('login', messages=messages))
        else:
            messages = {"main":"*user id or user name fail please try again"}
            session['messages'] = messages
            return redirect(url_for('login', messages=messages))
    else:
        messages = {"main":"*wrong email format please try again"}
        session['messages'] = messages
        return redirect(url_for('login', messages=messages))

@app.route("/bookingservice_duration", methods=['POST'])
def bookingservice_duration():
    service = request.form['service_duration']
    session['service'] = service
    return redirect(url_for('booking',service=service))

@app.route("/bookingservice_price", methods=['POST'])
def bookingservice_price():
    service = request.form['service_price']
    session['service'] = service
    return redirect(url_for('booking',service=service))

@app.route("/bookingstaff_score", methods=['POST'])
def bookingstaff_score():
    staff = request.form['staff_score']
    session['staff'] = staff
    return redirect(url_for('booking',staff=staff))

@app.route("/bookingstaff_price", methods=['POST'])
def bookingstaff_price():
    staff = request.form['staff_price']
    session['staff'] = staff
    return redirect(url_for('booking',staff=staff))

@app.route("/bookingstaff_exp", methods=['POST'])
def bookingstaff_exp():
    staff = request.form['staff_exp']
    session['staff'] = staff
    return redirect(url_for('booking',staff=staff))

@app.route("/bookingdate", methods=['POST'])
def bookingdate():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    seperator='-'
    dates = (str(year),str(month),str(day))
    if year == datetime.today().strftime('%Y'):
        if int(month) < int(datetime.today().strftime('%m')):
            staff=session['staff']    
            message = "*date not available today or before"
            session['message'] = message
            return redirect(url_for('booking',staff=staff, message=message))
        elif int(month) == int(datetime.today().strftime('%m')):
            if int(day) <= int(datetime.today().strftime('%d')):
                staff=session['staff']  
                message = "*date not available today or before"
                session['message'] = message
                return redirect(url_for('booking',staff=staff, message=message)) 
    try:
        date = datetime.strptime(seperator.join(dates), '%Y-%m-%d')
        week = date.strftime('%a').upper()
        staff=session['staff']
        sql="SELECT a.week, b.staff_name FROM working_week a, staff b WHERE a.staff = b.staff_ID and b.staff_name='%s'"%staff
        cursor.execute(sql)
        working_day=cursor.fetchall()
        for i in working_day:
            if i[0]==week:
                session['date'] = seperator.join(dates)
                return redirect(url_for('booking',date=seperator.join(dates)))
        suggestions=[]
        for i in working_day:
            suggestions.append(i[0])
        suggestion=seperator.join(suggestions)    
        message = "*date not available for this staff please change another day For example: "+suggestion
        session['message'] = message
        return redirect(url_for('booking',staff=staff,message=message))
    except:
        staff=session['staff']
        message = "*date not in correct format please try again"
        session['message'] = message
        return redirect(url_for('booking',staff=staff,message=message))

@app.route("/bookingtime", methods=['POST'])
def bookingtime():
    hour = request.form['hour']
    minute = request.form['minute']
    service = session['service']
    date = session['date']
    staff = session['staff']
    week = int(datetime.strptime(date, '%Y-%m-%d').weekday())
    sql = "SELECT duration FROM service WHERE service_name='%s'"%service
    cursor.execute(sql)
    service_time = cursor.fetchone()
    time_end = service_time[0] + timedelta(hours= int(hour), minutes=int(minute))
    sql1="SELECT a.booking_time , b.staff_name, c.duration FROM timetable a, staff b , service c WHERE a.staff = b.staff_ID and b.staff_name='%s' and a.booking_time LIKE '%s%%' and a.service=c.service_ID"%(staff,str(datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')))
    cursor.execute(sql1)
    busy_time=cursor.fetchall()
    print(busy_time)
    for i in busy_time:
        if timedelta(hours=int(datetime.strftime(i[0], '%H')),minutes=int(datetime.strftime(i[0], '%M'))) <= timedelta(hours=int(hour), minutes=int(minute)) < timedelta(hours=int(datetime.strftime(i[0], '%H')),minutes=int(datetime.strftime(i[0] ,'%M'))) + i[2]:
            print('1')
            message = "*time not available please change another time like after"+str(i[0]+i[2])
            session['message'] = message
            return redirect(url_for('booking',date=date,message=message))
        elif timedelta(hours=int(datetime.strftime(i[0],'%H')),minutes=int(datetime.strftime(i[0], '%M'))) < time_end <= timedelta(hours=int(datetime.strftime(i[0],'%H')),minutes=int(datetime.strftime(i[0],'%M'))) + i[2]:
            print('2')
            message = "*time not available please change another time like "+str(i[2])+" earlier"
            session['message'] = message
            return redirect(url_for('booking',date=date,message=message))
        elif timedelta(hours=int(hour), minutes=int(minute)) < timedelta(hours=int(datetime.strftime(i[0], '%H')),minutes=int(datetime.strftime(i[0], '%M'))):
            if time_end > timedelta(hours=int(datetime.strftime(i[0],'%H')),minutes=int(datetime.strftime(i[0],'%M'))) + i[2]:
                print('3')
                message = "*time not available please change another time like "+str(timedelta(hours=int(datetime.strftime(i[0],'%H')),minutes=int(datetime.strftime(i[0],'%M'))) + i[2])
                session['message'] = message
                return redirect(url_for('booking',date=date,message=message))
    if week==5 or week==6:
        if time_end > timedelta(hours = 19):
            lastest_time = timedelta(hours = 19) - service_time[0]
            message = "*time not available please change another time For example: "+str(lastest_time)
            session['message'] = message
            return redirect(url_for('booking',date=date,message=message))
    else:
        if time_end > timedelta(hours = 17):
            lastest_time = timedelta(hours = 17) - service_time[0]
            message = "*time not available please change another time For example: "+str(lastest_time)
            session['message'] = message
            return redirect(url_for('booking',date=date, message=message))
    time = str(hour)+':'+str(minute)+':00'
    session['time'] = time
    return redirect(url_for('booking',time=time))

@app.route("/bookingseat", methods=['POST'])
def bookingseat():
    seat = request.form['seat']
    session['seat'] = seat
    return redirect(url_for('booking',seat=seat))

@app.route("/bookingcancel", methods=['POST'])
def bookingcancel():
    return redirect(url_for('booking'))

@app.route("/bookingFunction", methods=['POST'])
def bookingFunction():
    service_name = session['service']
    staff_name = session['staff']
    date = session['date']
    time = session['time']
    seat = session['seat']
    booking_time = str(date)+' '+str(time)
    sql="SELECT service_ID FROM service WHERE service_name='%s'"%service_name
    cursor.execute(sql)
    service=cursor.fetchone()
    sql1="SELECT staff_ID FROM staff WHERE staff_name='%s'"%staff_name
    cursor.execute(sql1)
    staff=cursor.fetchone()
    if session.get('member'):
        sql2="INSERT INTO timetable (service,staff,booking_time,seat,member) VALUES (%s,%s,%s,%s,%s)"
        val=(service[0],staff[0],booking_time,seat,session['member'])
        cursor.execute(sql2,val)
        db.commit()
    else:
        sql2="INSERT INTO timetable (service,staff,booking_time,seat) VALUES (%s,%s,%s,%s)"
        val=(service[0],staff[0],booking_time,seat)
        cursor.execute(sql2,val)
        db.commit()
    success = "booking success"
    session['success'] = success
    return redirect(url_for('booking', success=success))

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/adminlogout", methods=['POST'])
def adminlogout():
    session.pop('admin',None)
    return redirect(url_for('index'))

@app.route("/timetable")
def timetable():
    try:
        month = request.args['month']
        year = request.args['year']
        firstday =  datetime.strptime(str(year)+'-'+str(month)+'-'+'01', '%Y-%m-%d')
        month_eng = datetime.strftime(firstday, '%B')
        firstday_week = firstday.weekday()
        month_days = int(calendar.monthrange(int(year), int(month))[1])
        days = []
        while int(firstday_week) > 0:
            days.append('')
            firstday_week = int(firstday_week)-1
        for i in range(1,month_days+1):
            days.append(i)
        session['month']=month
        session['year']=year
        try:
            start_time=request.args['start_time']
            end_time=request.args['end_time']
            day=request.args['day']
            time = []
            curr_time = start_time
            sql="SELECT staff_name FROM staff"
            cursor.execute(sql)
            staff=cursor.fetchall()
            print(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'))
            while timedelta(hours=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))) <= timedelta(hours=int(datetime.strftime(datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S'), '%M'))):
                staff_work = []
                details=[]
                print('2')
                for i in staff:
                    next_curr_time=datetime.strptime(str(timedelta(hours=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))) + timedelta(minutes=15)), '%H:%M:%S')
                    sql="SELECT a.staff_name, b.booking_time, c.duration, c.service_name, b.seat FROM staff a, timetable b, service c WHERE a.staff_ID=b.staff and c.service_ID=b.service and '%s'>b.booking_time and b.booking_time>='%s' and a.staff_name='%s'"%(datetime.strptime(str(year)+'-'+str(month)+'-'+str(day)+' '+str(datetime.strftime(datetime.strptime(str(next_curr_time), '%Y-%m-%d %H:%M:%S'), '%H:%M:%S')), '%Y-%m-%d %H:%M:%S'),datetime.strptime(str(year)+'-'+str(month)+'-'+str(day)+' '+str(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H:%M:%S')), '%Y-%m-%d %H:%M:%S'), i[0])
                    cursor.execute(sql)
                    result=cursor.fetchone()
                    print('3')
                    if result == None:
                        sql1="SELECT a.staff_name, b.booking_time, c.duration FROM staff a, timetable b, service c WHERE a.staff_ID=b.staff and c.service_ID=b.service and b.booking_time LIKE '%s%%' and a.staff_name='%s'"%(str(datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), '%Y-%m-%d').strftime('%Y-%m-%d')), i[0])
                        cursor.execute(sql1)
                        result1=cursor.fetchall()
                        endappend = 'N'
                        print(result1)
                        for j in result1:
                            if timedelta(hours=int(datetime.strftime(datetime.strptime(str(next_curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(next_curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))) > timedelta(hours=int(datetime.strftime(datetime.strptime(str(j[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(j[1]), '%Y-%m-%d %H:%M:%S'),'%M')))+timedelta(hours=int(datetime.strftime(datetime.strptime(str(j[2]), '%H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(j[2]), '%H:%M:%S'),'%M'))) >= timedelta(hours=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))):
                                staff_work.append('__end_work__')
                                details.append([])
                                endappend = 'Y'
                        if endappend == 'N':
                            staff_work.append('')
                            details.append([])
                    else:
                        sql1="SELECT a.staff_name, b.booking_time, c.duration, c.service_name FROM staff a, timetable b, service c WHERE a.staff_ID=b.staff and c.service_ID=b.service and b.booking_time LIKE '%s%%' and a.staff_name='%s'"%(str(datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), '%Y-%m-%d').strftime('%Y-%m-%d')), i[0])
                        cursor.execute(sql1)
                        result1=cursor.fetchall()
                        endappend = 'N'
                        for j in result1:
                            if timedelta(hours=int(datetime.strftime(datetime.strptime(str(next_curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(next_curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))) > timedelta(hours=int(datetime.strftime(datetime.strptime(str(j[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(j[1]), '%Y-%m-%d %H:%M:%S'),'%M')))+timedelta(hours=int(datetime.strftime(datetime.strptime(str(j[2]), '%H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(j[2]), '%H:%M:%S'),'%M'))) >= timedelta(hours=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))):
                                staff_work.append('__end&start_'+str(result[3])+'__')
                                details.append(result)
                                endappend = 'Y'
                        if endappend == 'N':
                            staff_work.append('__start_'+str(result[3])+'__')
                            details.append(result)
                print(staff_work)
                time.append((datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H:%M:%S'), staff_work,details))
                print('4')
                curr_time=datetime.strptime(str(timedelta(hours=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(curr_time), '%Y-%m-%d %H:%M:%S'), '%M'))) + timedelta(minutes=15)), '%H:%M:%S')
            print('5')
            date_selected=session['timetable_day']
            return render_template('timetable.html', days=days, month=month_eng, year=year, staff=staff, time=time, date_selected=date_selected)
        except:
            return render_template('timetable.html', days=days, month=month_eng, year=year)
    except:
        today_month = datetime.strftime(datetime.today(), '%m')
        today_month_eng = datetime.strftime(datetime.today(), '%B')
        today_year = datetime.strftime(datetime.today(), '%Y')
        firstday_week = datetime.strptime(str(today_year)+'-'+str(today_month)+'-'+'01', '%Y-%m-%d').weekday()
        today_month_days = int(calendar.monthrange(int(today_year), int(today_month))[1])
        days = []
        while int(firstday_week) > 0:
            days.append('')
            firstday_week = int(firstday_week)-1
        for i in range(1,today_month_days+1):
            days.append(i)
        session['month']=today_month
        session['year']=today_year
        return render_template('timetable.html', days=days, month=today_month_eng, year=today_year)

@app.route("/nextmonth", methods=['POST'])
def nextmonth():
    curr_month = session['month']
    curr_year = session['year']
    next_month = int(curr_month)+1
    if next_month > 12:
        next_month = 1
        next_year = int(curr_year)+1
    else:
        next_year = int(curr_year)
    return redirect(url_for('timetable', month=next_month, year=next_year))

@app.route("/prevmonth", methods=['POST'])
def prevmonth():
    curr_month = session['month']
    curr_year = session['year']
    prev_month = int(curr_month)-1
    if prev_month < 1:
        prev_month = 12
        prev_year = int(curr_year)-1
    else:
        prev_year = int(curr_year)
    return redirect(url_for('timetable', month=prev_month, year=prev_year))

@app.route("/selectdate", methods=['POST'])
def selectdate():
    day = request.form['day']
    month = session['month']
    year = session['year']
    weekday = int(datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), '%Y-%m-%d').weekday())
    if weekday == 5 or weekday == 6:
        start_time = datetime.strptime('11:00:00', '%H:%M:%S')
        end_time = datetime.strptime('19:00:00', '%H:%M:%S')
    else:
        start_time = datetime.strptime('09:00:00', '%H:%M:%S')
        end_time = datetime.strptime('17:00:00', '%H:%M:%S')
    session['timetable_day']=str(year)+'-'+str(month)+'-'+str(day)
    return redirect(url_for('timetable', month=month, year=year, start_time=start_time, end_time=end_time, day=day))

@app.route("/historycancel", methods=['POST'])
def historycancel():
    cancel=request.form['cancel']
    sql="DELETE FROM timetable WHERE booking_time='%s' and seat='%s'"%(cancel[0],cancel[1])
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('history'))

@app.route("/staff")
def staff():
    staff_ID=session['staffs']
    sql="SELECT staff_name, staff_ID FROM staff WHERE staff_ID='%s'"%staff_ID
    cursor.execute(sql)
    staffs=cursor.fetchone()
    staff=staffs[0]
    return render_template('staff.html',staff=staff)

@app.route("/stafflogout", methods=['POST'])
def stafflogout():
    session.pop('staffs',None)
    return redirect(url_for('index'))

@app.route("/score")
def score():
    advscore = 0
    count=0
    try:
        score=request.args['score']
        score=session['sco']
        print(score)
        for i in score:
            if i[2] != None:
                advscore += int(i[2])
                count+=1
        if count != 0:
            advscore = advscore/count
        return render_template('score.html', score=score, advscore=advscore)
    except:
        if session.get('sco'):
            session.pop('sco', None)
        staff=session['staffs']
        sql="SELECT a.service_name, b.booking_time, b.score FROM service a, timetable b WHERE a.service_ID=b.service and b.staff='%s'"%staff
        cursor.execute(sql)
        score=cursor.fetchall()
        for i in score:
            if i[2] != None:
                advscore += int(i[2])
                count+=1
        if count != 0:
            advscore = advscore/count
        return render_template('score.html', score=score, advscore=advscore)
        

@app.route("/monthscore", methods=['POST'])
def monthscore():
    staff=session['staffs']
    sql="SELECT a.service_name, b.booking_time, b.score FROM service a, timetable b WHERE a.service_ID=b.service and b.staff='%s' and b.booking_time LIKE '%s%%'"%(staff,str(datetime.strftime(datetime.today(), '%Y-%m')))
    cursor.execute(sql)
    score=cursor.fetchall()
    print(score)
    session['sco']=score
    return redirect(url_for('score', score=score))
    
@app.route("/yearscore", methods=['POST'])
def yearscore():
    staff=session['staffs']
    sql="SELECT a.service_name, b.booking_time, b.score FROM service a, timetable b WHERE a.service_ID=b.service and b.staff='%s' and b.booking_time LIKE '%s%%'"%(staff,str(datetime.strftime(datetime.today(), '%Y')))
    cursor.execute(sql)
    score=cursor.fetchall()
    session['sco']=score
    return redirect(url_for('score', score=score))

@app.route("/membership")
def membership():
    try:
        message=request.args['message']
        return render_template('membership.html', message=message)
    except:
        try:
            mes=request.args['mes']
            return render_template('membership.html', mes=mes)
        except:
            return render_template('membership.html')

@app.route("/nomalmembership", methods=['POST'])
def nomalmembership():
    member_name = request.form['member_name']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    if password == confirmpassword:
        sql="SELECT member_ID FROM member ORDER BY member_ID DESC"
        cursor.execute(sql)
        member_ID=cursor.fetchone()
        member_ID=member_ID[0]
        member_ID=int(member_ID[1]+member_ID[2]+member_ID[3]+member_ID[4]+member_ID[5]+member_ID[6]+member_ID[7])+1
        seperator=''
        lists=[]
        for i in str(member_ID):
            lists.append(i)
        while len(lists) < 7:
            lists.insert(0,'0')
        lists.insert(0,'M')
        member_ID=seperator.join(lists)
        sql="INSERT INTO member (member_ID, member_name, password, membership) VALUES (%s, %s, %s, %s)"
        val=(member_ID, member_name, password, '1')
        cursor.execute(sql,val)
        db.commit()
        message="success registor"
    else:
        message="password not same"
    return redirect(url_for('membership', message=message))

@app.route("/VIPmembership", methods=['POST'])
def VIPmembership():
    member_ID = request.form['member_ID']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    if password == confirmpassword:
        sql="SELECT * FROM member WHERE member_ID='%s' and password='%s'"%(member_ID,password)
        cursor.execute(sql)
        result=cursor.fetchone()
        if result != None:
            sql2="SELECT * FROM timetable WHERE member = '%s'"%member_ID
            cursor.execute(sql2)
            record = cursor.fetchall()
            count=0
            for i in record:
                count+=1
            if count <= 10:
                sql="UPDATE member SET membership='2' WHERE member_ID='%s' and password='%s'"%(member_ID,password)
                cursor.execute(sql)
                db.commit()
                mes="upgrade success"
            else:
                mes="requirement not enougth to upgrade"
        else:
            mes="wrong password or userID"
    else:
        mes="password not same"
    return redirect(url_for('membership',mes=mes))

@app.route("/POS")
def POS():
    try:
        payment = request.args['payment']
        done="process done"
        session['POS_done']=done
        return render_template('POS.html', done=done)
    except:
        try:
            member = request.args['member_ID']
            price = session['POS_price']
            member = session['POS_member']
            seat = session['POS_seat']
            staff = session['POS_staff']
            service = session['POS_service']
            try:
                mes=request.args['mes']
                mes="wrong ID or password"
                return render_template('POS.html', service=service, staff=staff, seat=seat, price=price, mes=mes)
            except:
                return render_template('POS.html', service=service, staff=staff, seat=seat, price=price)
        except:
            try:
                seat = request.args['seat']
                member = session['POS_member']
                seat = session['POS_seat']
                staff = session['POS_staff']
                service = session['POS_service']
                try:
                    mes=request.args['mes']
                    mes="wrong ID or password"
                    return render_template('POS.html', service=service, staff=staff, seat=seat, mes=mes)
                except:
                    return render_template('POS.html', service=service, staff=staff, seat=seat)
            except:
                try:
                    staff = request.args['staff']
                    seat = session['POS_seat']
                    staff = session['POS_staff']
                    service = session['POS_service']
                    return render_template('POS.html', service=service, staff=staff, seat=seat)
                except:
                    try:
                        service = request.args['service']
                        staff = session['POS_staff']
                        service = session['POS_service']
                        return render_template('POS.html', service=service, staff=staff)
                    except:
                        if session.get('POS_staff'):
                            session.pop('POS_staff', None)
                        if session.get('POS_service'):
                            session.pop('POS_service', None)
                        if session.get('POS_seat'):
                            session.pop('POS_seat', None)
                        if session.get('POS_member'):
                            session.pop('POS_member', None)
                        if session.get('POS_price'):
                            session.pop('POS_price', None)
                        if session.get('POS_done'):
                            session.pop('POS_done', None)
                        sql="SELECT service_name, price, duration FROM service"
                        cursor.execute(sql)
                        result=cursor.fetchall()
                        now=datetime.now()
                        weekday = int(now.weekday())
                        print(timedelta(hours=int(datetime.strftime(now,'%H')), minutes=int(datetime.strftime(now,'%M'))))
                        service=[]
                        imgs=[]
                        service_img=[]
                        if weekday == 5 or weekday == 6:  
                            end_time = datetime.strptime('19:00:00', '%H:%M:%S')
                        if weekday == 0 or weekday ==1 or weekday ==2 or weekday == 3 or weekday == 4:
                            end_time = datetime.strptime('17:00:00', '%H:%M:%S')
                        for i in result:
                            if timedelta(hours=int(datetime.strftime(now,'%H')), minutes=int(datetime.strftime(now,'%M')))+timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%M'))) <= timedelta(hours=int(datetime.strftime(datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S'), '%H')), minutes=int(datetime.strftime(datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S'), '%M'))):
                                service.append(i[0])
                                try:
                                    img = open('static/img/' + 'POS' + i[0]  + '.' + 'png')
                                    img.close()
                                    imgs.append('png')
                                except:
                                    try:
                                        img = open('static/img/' + 'POS' + i[0] + '.' + 'jpg')
                                        img.colse()
                                        imgs.append('jpg')
                                    except:
                                        try:
                                            img = open('static/img/' + 'POS' + i[0] + '.' + 'jpeg')
                                            img.colse()
                                            imgs.append('jpeg')
                                        except:
                                            imgs.append('png')
                        service_img.append(service)
                        service_img.append(imgs)
                        return render_template('POS.html', service_img=service_img)

@app.route("/POS_service", methods=['POST'])
def POS_service():
    service=request.form['service']
    now=datetime.now()
    today=datetime.today()
    sql="SELECT a.staff_name, c.booking_time, b.duration FROM staff a, service b, timetable c WHERE a.staff_ID=c.staff and b.service_ID=c.service and b.service_name='%s' and c.booking_time LIKE '%s%%'"%(service,today.strftime('%Y-%m-%d'))
    cursor.execute(sql)
    result=cursor.fetchall()
    staff=[]
    busy=[]
    week= now.strftime('%a').upper()
    print(week)
    sql="SELECT a.staff_name, b.week, c.service, d.service_name FROM staff a, working_week b, score c, service d WHERE a.staff_ID=b.staff and b.week='%s' and c.staff=a.staff_ID and c.service=d.service_ID and d.service_name='%s'"%(week,service)
    cursor.execute(sql)
    result1=cursor.fetchall()
    print(result1)
    for k in result1:
        add_staff="Y"
        for j in busy:
            if j==k[0]:
                add_staff="N"
        if add_staff=="Y":
            staff.append(k[0])
            print(staff)
    for i in result:
        if timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%M')))+timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%M'))) > timedelta(hours=int(datetime.strftime(now, '%H')), minutes=int(datetime.strftime(now, '%M'))) >= timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%M'))):
            add_busy="Y"
            for j in busy:
                if j==i[0]:
                    add_busy="N"
            if add_busy=="Y":
                busy.append(i[0])
    print(busy)
    for i in staff:  
        for j in busy:
            if j==i:
                staff.remove(i)
    session['POS_staff']=staff
    session['POS_service']=service
    print(staff)
    return redirect(url_for('POS', service=service))

@app.route("/POS_staff", methods=['POST'])
def POS_staff():
    staff=request.form['staff']
    now=datetime.now()
    sql="SELECT b.seat, b.booking_time, a.duration FROM service a, timetable b WHERE a.service_ID=b.service"
    cursor.execute(sql)
    result=cursor.fetchall()
    sql="SELECT * FROM seat"
    cursor.execute(sql)
    result1=cursor.fetchall()
    busy=[]
    seat=[]
    for k in result1:
        seat.append(k[0])
    for i in result:
        if timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%M')))+timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[2]), '%H:%M:%S'),'%M'))) > timedelta(hours=int(datetime.strftime(now, '%H')), minutes=int(datetime.strftime(now, '%M'))) >= timedelta(hours=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%H')), minutes=int(datetime.strftime(datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S'),'%M'))):
            add_busy="Y"
            for j in busy:
                if j == i[0]:
                    add_busy="N"
            if add_busy == "Y":
                busy.append(i[0])
    for i in seat:
        for j in busy:
            if j==i:
                seat.remove(i)
    print(seat)
    session['POS_seat']=seat
    session['POS_staff']=staff
    return redirect(url_for('POS', staff=staff))

@app.route("/POS_seat", methods=['POST'])
def POS_seat():
    seat=request.form['seat']
    session['POS_seat']=seat
    member="Y"
    session['POS_member']=member
    return redirect(url_for('POS', seat=seat))

@app.route("/POS_member", methods=['POST'])
def POS_member():
    member_ID = request.form['member_ID']
    member_password = request.form['member_password']
    submit = request.form['submit']
    sql="SELECT a.member_ID, a.password, b.discount FROM member a, membership b WHERE a.membership=b.membership_ID"
    cursor.execute(sql)
    member=cursor.fetchall()
    if submit == "member":
        for i in member:
            if i[0]==member_ID and i[1]==member_password:
                seat=session['POS_seat']
                staff=session['POS_staff']
                service=session['POS_service']
                now=datetime.now()
                sql="SELECT a.price, c.price, b.seat FROM service a, timetable b, staff c WHERE a.service_ID=b.service and c.staff_ID=b.staff and a.service_name='%s' and a.staff_name='%s'"%(service,staff)
                cursor.execute(sql)
                result=cursor.fetchone()
                price=(result[0] +result[1])/i[2]
                session['POS_price']=price
                member=i[0]
                session['POS_member']=member
                return redirect(url_for('POS',member_ID=member_ID))
        member=session['POS_member']
        mes="Y"
        return redirect(url_for('POS', seat=seat, mes=mes))
    elif submit == "skip":
        seat=session['POS_seat']
        staff=session['POS_staff']
        service=session['POS_service']
        now=datetime.now()
        sql="SELECT price, service_ID FROM service WHERE service_name='%s'"%service
        cursor.execute(sql)
        result=cursor.fetchone()
        sql="SELECT price, staff_ID FROM staff WHERE staff_name='%s'"%staff
        cursor.execute(sql)
        result1=cursor.fetchone()
        price=result[0] +result1[0]
        session['POS_price']=price
        return redirect(url_for('POS',member_ID=member_ID))

@app.route("/POS_payment", methods=['POST'])
def POS_payment():
    payment=request.form['payment']
    seat = session['POS_seat']
    staff = session['POS_staff']
    service = session['POS_service']
    member=session['POS_member']
    sql="SELECT service_ID, service_name FROM service WHERE service_name='%s'"%service
    cursor.execute(sql)
    service_name=cursor.fetchone()
    sql="SELECT staff_ID, staff_name FROM staff WHERE staff_name='%s'"%staff
    cursor.execute(sql)
    staff_name=cursor.fetchone()
    now=datetime.now()
    if member == "Y":
        sql="INSERT INTO timetable (service, staff, booking_time, seat) VALUES ('%s','%s','%s','%s')"%(service_name[0],staff_name[0],now,seat)
        cursor.execute(sql)
        db.commit()
        done="done"
        return redirect(url_for('POS',payment=payment))
    else:
        sql="INSERT INTO timetable (service, staff, booking_time, seat, member) VALUES ('%s','%s','%s','%s','%s')"%(service_name[0],staff_name[0],now,seat,member)
        cursor.execute(sql)
        db.commit()
        done="done"
        return redirect(url_for('POS',payment=payment))

@app.route("/POS_cancel", methods=['POST'])
def POS_cancel():
    return redirect(url_for('POS'))

if __name__ == "__main__":
    app.run(host='192.168.1.3', port='80', debug=True)
