from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
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
                sender='allen.kumarmohit@gmail.com',
                recipients=[reciver])
    msg.body="Here is your password :"+str(passw)
    mail.send(msg)
    flash('password sent succesfully please log in')
    return
#session['hostel']='HALL OF RESIDENCE'
@app.before_first_request
def init_app():
    session['hostelname'] = 'HALL OF RESIDENCE'


@app.route('/')
def home():
    return render_template('home.html')
    #return redirect(url_for('login'))
@app.route('/apj')
def apj():
    session['hostelname']='A. P. J ABDUL KALAM HALL OF RESIDENCE'
    return redirect(url_for('home'))
@app.route('/vsb')
def vsb():
    session['hostelname']='VIKRAM SARABHAI HALL OF RESIDENCE'
    return redirect(url_for('home'))

@app.route('/cvr')
def cvr():
    session['hostelname']='C. V. RAMAN HALL OF RESIDENCE'
    return redirect(url_for('home'))

@app.route('/devi')
def devi():
    session['hostelname']='DEVI AHILYA HALL OF RESIDENCE'
    return redirect(url_for('home'))

@app.route('/homi')
def homi():
    session['hostelname']='HOMI JEHANGIR BHABHA HALL OF RESIDENCE'
    return redirect(url_for('home'))

@app.route('/jcb')
def jcb():
    session['hostelname']='J. C. BOSE HALL OF RESIDENCE'
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
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
            if(data[3]==password):
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
    return redirect(url_for('home'))

@app.route('/signup',methods=["GET","POST"])
def signup():
    if(request.method=='POST'):
        #add to data base
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        if(len(username)==0 or len(email)==0 or len(password)==0):
            flash('enter a valid details')
            return redirect(url_for('signup'))
        cur=mysql.connection.cursor()
        #print(username,password,email)
        x=cur.execute("SELECT * FROM users WHERE username=(%s)",(username,))
        if(int(x)>0):
            flash("USERNAME ALREADY EXIST PLEASE USE ANOTHER")
            return render_template('signup.html')
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            flash("USER ALREADY REGISTERED WITH THIS EMAIL ID")
            return render_template('signup.html')
        cur.execute("INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",(username,email,password))
        mysql.connection.commit()
        cur.close()
        flash('successfully registered please login')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/forgot-password',methods=['GET','POST'])
def forgotpassword():
    if(request.method=='POST'):
        email = request.form.get('email')
        #print(email)
        cur = mysql.connection.cursor()
        # print(username,password,email)
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            data = cur.fetchone()
            send_mail(email, data[3])
            return redirect(url_for('login'))
        else:
            flash('Email not registered')
            return render_template('forgotpassword.html')
    return render_template('forgotpassword.html')
app.run(debug=True)