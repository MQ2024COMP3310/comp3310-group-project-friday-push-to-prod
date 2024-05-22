from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from .models import Photo
from sqlalchemy import asc, text
from . import db
import os

auth = Blueprint('auth', __name__)

# Sign Up Page and sign up form submission
@auth.route('/signup/', methods = ['GET', 'POST'])
def signUp():
  if request.method == 'POST':

    return redirect(url_for('main.homepage'))

    # Return below if invalid input
    #return render_template('signup.html', error = "Invalid Input, Try Again!")
  else:
    return render_template('signup.html')
