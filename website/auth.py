from email.mime.text import MIMEText

from flask import Blueprint,render_template, request, redirect,flash,url_for
from .models import *
from flask_login import login_user,login_required,logout_user,current_user
from . import utils
import re

auth = Blueprint('auth',__name__)
pass_regex = '[A-Za-z0-9@#$%^&+=]{8,}'

#input : None
#output : inserts a new record in user table
@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        #store the data from the form
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['password-repeat']
        username = request.form['username']
        #see if the user's email is already in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            if password == repeat_password:
                if re.match(pass_regex,password):
                    try:
                        print("error 500 debugging")
                        new_user = User(email=email, password=utils.encryptText(password), username=username)
                        db.session.add(new_user)
                        db.session.commit()
                        #login the user in the current session
                        login_user(user=new_user)
                        #sends an email with a token code to the user
                        with utils.initMailServer() as server:
                            token = utils.encryptText(email)
                            message = utils.createEmailObject("Email confirmare cont",utils.MAIL,email,"Codul tau este : "+token)
                            server.sendmail(utils.MAIL,email,message.as_string())

                        flash('Te rugam sa confirmi email-ul pentru a-ti activa contul.')
                        return redirect('/activateaccount')
                    except Exception as e:
                        flash(e)
                        return redirect('/register')
                else:
                    flash("Parola trebuie sa contina \n")
                    flash("1. cel putin o lungime de 8 caractere dar nu mai mult de 32 de caractere.\n")
                    return redirect('/register')
            else:
                flash("Parole nu corespund.")
                return redirect('/register')
        else:
            flash("Email-ul este deja folosit pe site-ul nostru.")
            return redirect('/register')

#input : None
#output : GET : returns a template containg form for login
#         POST : check the credentials and login the user
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if utils.encryptText(password) == user.password:
                flash("Te-ai logat cu succes")
                login_user(user,remember=True)
                return redirect('/')
            else:
                flash("Email sau parola gresite.")
                return redirect('/login')
        else:
            flash("Email sau parola gresite.")
            return redirect('/login')

#input : None
#output : GET : just logout the current logged user
@auth.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    if current_user.is_authenticated:
        flash('Te-ai delogat de pe contul tau')
    return redirect(url_for('auth.login'))

#input : None
#output : GET : returns a template containg form for introducing the token code (from mail)
@auth.route('/activateaccount',methods=['GET','POST'])
def activateToken():
    #check if the hash of current user email is equal with token code -> activate
    if request.method == 'GET':
        return render_template('activateaccount.html')
    # get the current's user email
    input_email = request.form['token']
    if input_email.strip() == utils.encryptText(current_user.email):
        current_user.activated = True
        db.session.commit()
        return redirect('/')
    flash("Codul de activare introdus este gresit")
    return redirect('/activateaccount')

