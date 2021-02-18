from email.mime.text import MIMEText

from flask import Blueprint,render_template, request, redirect,flash,url_for
from .models import *
from flask_login import login_user,login_required,logout_user,current_user
from email.message import EmailMessage
import hashlib,smtplib

MAIL = "silviu.dinca20@gmail.com"
PASSW = "23SDFFFxx323"

auth = Blueprint('auth',__name__)

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['password-repeat']
        username = request.form['username']
        user = User.query.filter_by(email=email).first()
        if not user:
            if password == repeat_password:
                try:
                    new_user = User(email=email, password=encryptText(password), username=username)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(user=new_user)
                    with initMailServer() as server:
                        token = encryptText(email)
                        message = createEmailObject("Email confirmare cont",MAIL,email,"Codul tau este : "+token)
                        server.sendmail(MAIL,email,message.as_string())

                    flash('Te rugam sa confirmi email-ul pentru a-ti activa contul.')
                    return redirect('/activateaccount')
                except:
                    pass
            else:
                flash("Parole nu corespund.")
                return redirect('/register')
        else:
            flash("Email-ul este deja folosit pe site-ul nostru.")
            return redirect('/register')

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if encryptText(password) == user.password:
                flash("Te-ai logat cu succes")
                login_user(user,remember=True)
                return redirect('/')
            else:
                flash("Email sau parola gresite.")
                return redirect('/login')
        else:
            flash("Email sau parola gresite.")
            return redirect('/login')
@auth.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    if current_user.is_authenticated:
        flash('Te-ai delogat de pe contul tau')
    return redirect(url_for('auth.login'))

@auth.route('/activateaccount',methods=['GET','POST'])
def activateToken():
    #iau email-ul user-ului curent
    #daca ce se introduce in form e egal cu hash-ul email-ului
    #inseamna ca e ok .
    if request.method == 'GET':
        return render_template('activateaccount.html')
    input_email = request.form['token']
    if input_email.strip() == encryptText(current_user.email):
        current_user.activated = True
        db.session.commit()
        return redirect('/')
    flash("Codul de activare introdus este gresit")
    return redirect('/activateaccount')

#input :  plaintext - string - the text we want to hash
#output : result : string - the unique hash specific to input
def encryptText(plaintext):
    result = hashlib.sha1(plaintext.encode('utf-8'))
    return result.hexdigest()

def initMailServer():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL, PASSW)
    return server

def createEmailObject(subject,fromm,to,content):
    result = EmailMessage()
    result['subject'] = subject
    result['from'] = fromm
    result['to'] = to
    html = '<h1>' + content + '</h1>'
    result.set_content(html,subtype='html')
    return result