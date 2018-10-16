from flask import Flask, render_template,request
import pymysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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

    if request.method==  'POST':
       flag=0
       username=request.form['username']
       password=request.form['pass']
       cursor.execute('SELECT * FROM login')
       login=cursor.fetchall()
       print(login)
       for row in  login:
           if username == row[0] and password == row[1]:
             flag=1

    db.close()
    if flag==1:
        return "HELLOO Login Successful!"
    else:
        return "Login Unsuccessful"

if __name__ == '__main__':
    app.run(debug=True)
