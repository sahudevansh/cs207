from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import random
app=Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'abc'
mysql=MySQL(app)

app.secret_key="qwertyuiopasdfghjklzxcvbnm"

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='cs207hostelproject@gmail.com',
    MAIL_PASSWORD='cs207dbms'
)

mail=Mail(app)
def send_mail(reciver,passw):
    msg=Message('Password',
                sender='cs207hostelproject@gmail.com',
                recipients=[reciver])
    msg.body="Here is your password :"+str(passw)
    mail.send(msg)
    flash('password sent succesfully please log in')
    return

def send_otp(reciver,otp):
    msg=Message('OTP',
                sender='cs207hostelproject@gmail.com',
                recipients=[reciver])
    msg.body="Here is your one time password :"+str(otp)
    mail.send(msg)
    flash('otp sent succesfully please validate')
    return



@app.before_first_request
def init_app():
    session['hostelname'] = 'WELCOME TO IIT INDORE'
    session['show'] = True
    session['logged_in'] =False
    session['signup']=False
    session['otpverify'] = False
@app.route('/')
def home():
    session['show'] = True
    session['hostelname'] = 'WELCOME TO IIT INDORE'
    return render_template('home.html')
    #return redirect(url_for('login'))
@app.route('/apj')
def apj():
    session['show'] = False
    session['hostelname']='A. P. J ABDUL KALAM'
    return render_template('apj.html')
@app.route('/vsb')
def vsb():
    session['hostelname']='VIKRAM SARABHAI'
    return render_template('vsb.html')

@app.route('/cvr')
def cvr():
    session['hostelname']='C. V. RAMAN'
    return render_template('cvr.html')

@app.route('/devi')
def devi():
    session['hostelname']='DEVI AHILYA'
    return render_template('devi.html')

@app.route('/homi')
def homi():
    session['hostelname']='HOMI JEHANGIR BHABHA'
    return render_template('homi.html')

@app.route('/jcb')
def jcb():
    session['hostelname']='J. C. BOSE'
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        #print(username,password)
        cur1 = mysql.connection.cursor()
        #print(cur1)
        x=cur1.execute("SELECT * FROM users WHERE username=%s",(username,))
        #print(x)
        if (x!=0):
            data=cur1.fetchone()
            #print(data)
            if(data[2]==password):
                session['username'] = data[0]
                session['logged_in']=True
                return redirect(url_for('home'))
            else:
                flash('wrong password')
                return render_template('login.html')
        else:
            flash('user not registered')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in']=False
    session['otpverify'] = False
    session['signup'] = False
    return redirect(url_for('home'))
@app.route('/userdetails',methods=["GET","POST"])
def userdetails():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if ('signup' in session and session['signup'] == False):
        flash('PLEASE SIGNUP FIRST TO ENTER DETAILS')
        return redirect('signup')
    if ('otp' in session and session['otp'] == False):
        flash('please veryfiy the otp first')
        return redirect(url_for('otp'))
    if(request.method=='POST'):
        name=request.form.get('fullname')
        rollno=request.form.get('rollno')
        branch=request.form.get('branch')
        hostelname=request.form.get('hostelname')
        roomno=request.form.get('roomno')
        mobileno=request.form.get('mobileno')
        if(len(name)==0 or len(rollno)==0 or len(branch)==0 or len(hostelname)==0 or len(roomno)==0 or len(mobileno)==0):
            flash('enter a valid details')
            return redirect(url_for('userdetails'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username,email,password,name,rollno,branch,hostelname,roomno,mobileno) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (session['username'],session['email'], session['password'],name,rollno,branch,hostelname,roomno,mobileno))
        mysql.connection.commit()
        cur.close()
        session['logged_in'] = True
        return redirect(url_for('home'))
    return render_template('userdetails.html')


@app.route('/otpverification',methods=['GET','POST'])
def otp():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if ('signup' in session and session['signup'] == False):
        flash('PLEASE SIGNUP FIRST TO ENTER DETAILS')
        return redirect('signup')
    if(request.method=='POST'):
        num=request.form.get('otp')
        #print(num,session['otp'])
        if(int(num)==session['otp']):
            session['otpverify']=True
            session['signup'] = True
            flash('Successfully registered please enter your details')
            return redirect(url_for('userdetails'))
        else:
            flash('OTP ENTERED IS INCORRECT')
            return render_template('otpverify.html')
    return render_template('otpverify.html')


@app.route('/signup',methods=["GET","POST"])
def signup():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        #add to data base
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        '''if(email[-10:]!='iiti.ac.in'):
            flash('Please use institute mail id only')
            return redirect(url_for('signup'))'''
        if(len(username)==0 or len(email)==0 or len(password)==0):
            flash('enter a valid details')
            return redirect(url_for('signup'))
        cur=mysql.connection.cursor()
        x=cur.execute("SELECT * FROM users WHERE username=(%s)",(username,))
        if(int(x)>0):
            flash("USERNAME ALREADY EXIST PLEASE USE ANOTHER")
            return render_template('signup.html')
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            flash("USER ALREADY REGISTERED WITH THIS EMAIL ID")
            return render_template('signup.html')
        cur.close()
        x1=random.randrange(111111,999999)
        send_otp(email,x1)
        #d={'x':x1,'username':username,'email':email,'password':password}
        session['username'] = username
        session['email'] = email
        session['password'] = password
        session['otp']=x1
        session['otpverify'] = False
        session['signup'] = True
        return redirect(url_for('otp'))
    return render_template('signup.html')

@app.route('/forgot-password',methods=['GET','POST'])
def forgotpassword():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        email = request.form.get('email')
        cur = mysql.connection.cursor()
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            data = cur.fetchone()
            send_mail(email, data[2])
            return redirect(url_for('login'))
        else:
            flash('Email not registered')
            return render_template('forgotpassword.html')
    return render_template('forgotpassword.html')
@app.route('/complaints',methods=['GET','POST'])
def complaints():

    if('logged_in' in session and session['logged_in']==False):
        flash('PLEASE LOG IN FIRST')
        return redirect(url_for('login'))
    session['hostelname']='REGISTER YOUR COMPLAINTS'
    session['show']=True
    if(request.method=='POST'):
        subject=request.form.get('subject')
        category=request.form.get('category')
        timeofavilibility=request.form.get('timeofavial')
        urgency=request.form.get('urgency')
        details=request.form.get('details')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO complaints(username,subject,category,time_of_availability,uergency,details) VALUES(%s,%s,%s,%s,%s,%s)",(session['username'],subject,category,timeofavilibility,urgency,details))
        mysql.connection.commit()
        cur.close()
        flash('Complaint registered')
        return render_template('complaints.html',scrollToAnchor='contact')

    return render_template('complaints.html')

@app.route('/suggetions',methods=['GET','POST'])
def suggetions():
    if('logged_in' in session and session['logged_in']==False):
        flash('PLEASE LOG IN FIRST')
        return redirect(url_for('login'))
    session['hostelname']='PROVIDE YOUR VALUEABLE SUGGETIONS'
    session['show']=True
    if(request.method=='POST'):
        subject=request.form.get('subject')
        category=request.form.get('category')
        details=request.form.get('details')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO suggetions(username,subject,category,details) VALUES(%s,%s,%s,%s)",(session['username'],subject,category,details))
        mysql.connection.commit()
        cur.close()
        flash('THANK YOU FOR YOUR VALUEABLE SUGGETION WE WILL IMPORVE OURSELEVES')
        return render_template('suggetions.html',scrollToAnchor='contact')

    return render_template('suggetions.html')


app.run(debug=True)