from flask import Blueprint,render_template, request, redirect,flash,url_for
from .models import *
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['password-repeat']
        new_user = User(email=email,password=password,username='x')
        user = User.query.filter_by(email=email).first()
        if not user:
            if password == repeat_password:
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(user=new_user)
                    flash('Te-ai inregistrat cu succes !')
                    return redirect('/')
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
            if password == user.password:
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