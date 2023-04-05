from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import base64

app=Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password-123'
app.config['MYSQL_DB'] = 'schema'


app.secret_key = os.environ.get('SECRET_KEY')

mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('index.html')
	
	
@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('home'))


@app.route('/register' , methods =['GET', 'POST'])
def register():
	display_message=''
	
	if request.method =='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		email=request.form['email']
		uname=request.form['username']
		pswd=request.form['password']
		encoded_password = base64.b64encode(pswd.encode('utf-8')).decode('utf-8')
	
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('Select * from usertable where name = % s ' , (uname,))
		details=cursor.fetchone()
		
		if details:
			display_message='Acc already exists'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			display_message='Check your email address'
		elif not re.match(r'[A-Za-z0-9]+', uname):
			display_message='Username should be in characters and numbers only'
		elif not uname or not pswd or not email:
			display_message='Fill Form' 
		else:
			cursor.execute('Insert into usertable values (NULL, % s , % s ,% s )',(uname,email,encoded_password,))	
			mysql.connection.commit()
			display_message='Registered Successfully !!! '
				
		
		
	elif request.method == 'POST':
		display_message='Fill the form'
		
	
	return render_template('registration.html', display_message=display_message)
	
	
	
	
	
	
@app.route('/login', methods =['GET', 'POST'])
def login():
	display_message=''
	
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		uname=request.form['username']
		pswd=request.form['password']
		encoded_password = base64.b64encode(pswd.encode('utf-8')).decode('utf-8')
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('Select * from usertable where name = % s and password = %s ' , (uname,encoded_password,))
		details=cursor.fetchone()
		
		if details:
			session['loggedin'] = True
			session['id'] = details['userid']
			session['username'] = details['name']
			display_message='Logged in Successfully !'
			return redirect(url_for('samplepage'))
		else:
			display_message='Enter details correctly'
            		
			
		
	return render_template('login.html',display_message=display_message)
	
	
	
	



@app.route('/sample' , methods=['GET','POST'])
def samplepage():
	if 'loggedin' in session:
		if session['loggedin'] == True:
			return render_template('welcome.html')
		
	return redirect(url_for('login'))
		




	
	

	
	
	
	
	

if __name__ == '__main__':
	app.run(debug=True,port=5001)
