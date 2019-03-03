from flask import Flask, render_template,request,url_for
import pymysql
from config import Config
#import app1
import os
app = Flask(__name__)
app.config.from_object(Config)

username=""
@app.route('/')
def index():

    user = {'username': 'Miguel'}
    return  render_template('index.html',user=user,title='Home')



@app.route('/handle_data', methods=['GET','POST'])
def handle_data():
    login=[]
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)
    flag=3
    if request.method==  'POST' and request.form['submit']== "login":
       flag=0
       username=request.form['username']
       password=request.form['pass']
       selectt=request.form.get('selectt')
       cursor.execute('SELECT * FROM login')
       login=cursor.fetchall()
       print(login)
       for row in  login:
           if username == row[0] and password == row[1] and  selectt== row[2] and  selectt =="Doctor" :
             flag=1
           if username == row[0] and password == row[1] and  selectt== row[2] and  selectt =="Receiptionist" :
             flag=2
           if username == row[0] and password == row[1] and  selectt== row[2] and  selectt =="Admin" :
             flag=3
    db.close()
    if flag ==1:
        return sign_in_doc()
    elif flag == 2:
        return sign_in_recp()
    elif flag== 3:
        return sign_in_admin()
    else:
        return index()
@app.route('/')
def sign_in_recp():

    login = []
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING"')
    apt=cursor.fetchmany(5)
    cursor.execute("SELECT * FROM patient")
    pt=cursor.fetchall()
    db.commit()
    return  render_template('table1.html',appointment=apt,patient=pt)

@app.route('/questions', methods=['GET','POST'])
def find_questions():
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    #username=request.form['username']
    if request.form['submit'] == 'Cancel' and request.method == 'POST':
        cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING"')
        appointments = cursor.fetchall()
        appointments[0][0]
        new_status="Cancelled"
        cursor.execute('UPDATE appointment SET Status="Cancelled" WHERE apid=%s ',appointments[0][0])
        #for row in appointments:
            #print("app")
           # if request.form.get('status1') == "Completed" and request.form['loop'] == appointment.index(row):
                #print("complete")
                #cursor.execute('UPDATE appointment SET Status="Completed" Where apid=%s', row[0])
            #if request.form.get('status1') == "Cancelled":
                #print("cancel")
                #cursor.execute('UPDATE appointment SET Status="Cancelled" Where apid=%s', row[0])
                #cursor.execute('DELETE FROM appointment WHERE Status=="Cancelled"')


    if request.method == 'POST'and request.form['submit'] == 'Add':
       aptid=0
       aptname=request.form['name']
       aptdatetime=request.form['DateTime']
       aptdoctor=request.form.get('Doctor')
       status="UPCOMING"
       cursor.execute('SELECT * FROM patient')
       patients = cursor.fetchall()
       print(patients)
       aptptid=0
       for row in patients:
          if  row[1]==aptname:
              aptptid=row[0]

       cursor.execute('SELECT * FROM doctor')
       doctor = cursor.fetchall()
       print(doctor)
       aptdocid=0
       for row in doctor:
            if row[4] == aptdoctor:
                aptdocid = row[0]
       print(aptid,aptdatetime,aptdocid,aptptid,status)
       appointment=[]
       appointment.append(aptid)
       appointment.append(aptdatetime)
       appointment.append(aptdocid)
       appointment.append(aptptid)
       appointment.append(status)
       cursor.execute('INSERT INTO appointment(apid,apdatetime,Docid,Ptid,Status) VALUES(%s,%s,%s,%s,%s)', appointment)
    if request.method =='POST' and request.form['submit'] == 'Save':
        patientdetail=[]
        patientdetail.append(0)
        ptname=request.form['ptnname']
        patientdetail.append(ptname)
        patientdetail.append(request.form['ptmob'])
        patientdetail.append(request.form['ptage'])
        patientdetail.append(request.form.get('sex'))
        patientdetail.append(request.form.get('ptbdgrp'))
        cursor.execute('INSERT INTO patient(Ptid,name,mobno,age,sex,bloodgroup) VALUES(%s,%s,%s,%s,%s,%s)', patientdetail)




    db.commit()
    return sign_in_recp()
@app.route('/sign_in',methods=["POST"])
def sign_in_doc():

    login = []
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM doctor')
    doctor = cursor.fetchall()
    #cursor.execute("CREATE VIEW appointment_table  AS SELECT apt.apid,pt.name,apt.apdatetime,apt.status,doc.speciality FROM appointment AS apt INNER JOIN patient AS pt ON apt.Ptid=pt.Ptid INNER JOIN doctor AS doc ON apt.Docid=doc.Docid")

    cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING"')

    apt=cursor.fetchmany(5)
    cursor.execute('SELECT * FROM patient')
    patient = cursor.fetchall()
    return render_template('dashboard.html',appointment=apt,patient=patient)

@app.route('/pres',methods=['POST'])
def pres():
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    if request.form['submit']== "save"  and request.method == 'POST':
        pres=[0]
        pres.append(request.form['fees'])
        pres.append(request.form['treatment'])
        pres.append(request.form['suggestedtests'])
        doctor = request.form.get('doctor')
        cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING"')
        appointments = cursor.fetchall()
        pres.append(appointments[0][0])
        cursor.execute('INSERT INTO prescription(PrId,fee,treatment,test,ApId) VALUES(%s,%s,%s,%s,%s)', pres)
        print("HiiiIIi")

        cursor.execute('SELECT * FROM doctor WHERE speciality=%s',doctor)
        doctor = cursor.fetchone()
        cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING" AND Speciality=%s', doctor[4])
        appointments = cursor.fetchall()
        appointments[0][0]
        new_status = "Completed"
        cursor.execute('UPDATE appointment SET Status="Completed" WHERE apid=%s ', appointments[0][0])
    db.commit()
    return dash_form()

@app.route('/sign_in_admin',methods=['GET','POST'])
def sign_in_admin():
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM doctor')
    doctor=cursor.fetchall()
    cursor.execute('SELECT * FROM receptionist')
    receptionist = cursor.fetchall()
    totalfees=[]
    applen=[]
    for row in doctor:
        cursor.execute('SELECT * FROM appointment_table WHERE status="Completed" and speciality=%s',row[4])
        appointment=cursor.fetchall()
        fees=0
        for i in range(len(appointment)):
            fees = fees + int(row[5])
        applen.append(len(appointment))
        totalfees.append(fees)
    print(applen)
    print(totalfees)
    db.commit()
    return render_template('admin.html',doctor=doctor,totalfees=totalfees,applen=applen,receptionist=receptionist)

@app.route('/dashform')
def dash_form():
    print("here i am")
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patient")
    pt = cursor.fetchall()
    return  render_template('doctortable.html',patient=pt)

@app.route('/dashboard')
def dash_board():
    print("here i am")
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM doctor')
    doctor = cursor.fetchall()
    #cursor.execute("CREATE VIEW appointment_table  AS SELECT apt.apid,pt.name,apt.apdatetime,apt.status,doc.speciality FROM appointment AS apt INNER JOIN patient AS pt ON apt.Ptid=pt.Ptid INNER JOIN doctor AS doc ON apt.Docid=doc.Docid")
    cursor.execute('SELECT * FROM appointment_table WHERE status="UPCOMING" AND Speciality=%s ', doctor[0][4])
    apt = cursor.fetchmany(5)
    db.commit()
    return sign_in_doc()



@app.route('/ptsearch',methods=['POST'])
def ptsearch():
    db = pymysql.connect("localhost", "root", "Akanksha@19", "Akanksha")
    cursor = db.cursor()
    if  request.method == 'POST' and request.form['submit'] == "searchdt" :
        patient=request.form.get('patientname')
        cursor.execute('SELECT * FROM patient WHERE name=%s',patient)
        patients=cursor.fetchone()
        cursor.execute('SELECT * FROM appointment WHERE Ptid=%s', patient[0])
        appointment=cursor.fetchall()

        appointmentdetail=[]
        for row in appointment:
            appointmentde=[]
            cursor.execute('SELECT * FROM prescription WHERE ApId=%s', row[0])
            pres=cursor.fetchone()
            appointmentde.append(row[0])
            appointmentde.append(row[1])
            appointmentde.append(pres[2])
            appointmentde.append(pres[3])
            appointmentdetail.append(appointmentde)
        db.commit()
        return  render_template('dashboard.html',appointment=apt,patient=patients,patients=appointmentdetail)







if __name__ == '__main__':
    app.run(debug=True)

