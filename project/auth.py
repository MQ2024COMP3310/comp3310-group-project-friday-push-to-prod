from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from .models import User
from sqlalchemy import asc, text
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# Sign Up Page and sign up form submission
@auth.route('/signup/', methods = ['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    username = request.form.get('user')
    
    user = User.query.filter_by(username=username).first()
    if user:
      return render_template('signup.html', error = "User already exists navigate to /login")
    
    password = request.form.get('password')

    new_user = User(username = username, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.homepage'))

  else:
    return render_template('signup.html')
