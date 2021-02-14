from flask import Blueprint,render_template, request, redirect,flash
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
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/')

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
                login_user(user,remember=True)
                return redirect('/')
        else:
            return '<h1> wrong </h1>';