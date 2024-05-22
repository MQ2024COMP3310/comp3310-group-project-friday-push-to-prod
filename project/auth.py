from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from .models import User
from sqlalchemy import asc, text
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.homepage'))

# Login Page 
@auth.route('/login/', methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('user')
    
    user = User.query.filter_by(username=username).first() 
    password = request.form.get('password')

    if not user or not check_password_hash(user.password, password):
        flash("Invalid Login Details, Try Again!")
        return render_template('login.html')

    login_user(user)

    return redirect(url_for('main.homepage'))
  else:
    return render_template('login.html')

# Sign Up Page and sign up form submission
@auth.route('/signup/', methods = ['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    username = request.form.get('user')
    
    user = User.query.filter_by(username=username).first()
    if user:
      flash("User already exits navigate to /login")
      return render_template('signup.html')
    
    password = request.form.get('password')

    new_user = User(username = username, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect(url_for('main.homepage'))

  else:
    return render_template('signup.html')
