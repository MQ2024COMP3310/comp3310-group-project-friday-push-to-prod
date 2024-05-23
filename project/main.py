from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from .models import Photo, User, Like
from sqlalchemy import asc, text
from . import db
import os
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

# This is called when the home page is rendered. It fetches all images sorted by filename.
@main.route('/')
def homepage():
  photos = db.session.query(Photo).filter_by(private = False).order_by(asc(Photo.file))
  return render_template('index.html', photos = photos)

@main.route('/uploads/<name>')
def display_file(name):
  response = make_response(send_from_directory(current_app.config["UPLOAD_DIR"], name))

  photo = db.session.query(Photo).filter_by(file = name).one()
  # Add header to response to prevent search engines from indexing the image if it is private
  if photo.private:
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
  return response

# Upload a new photo
@main.route('/upload/', methods=['GET','POST'])
# If user not logged in they will be redirected to /login 
@login_required
def newPhoto():
  if request.method == 'POST':
    file = None
    if "fileToUpload" in request.files:
      file = request.files.get("fileToUpload")
    else:
      flash("Invalid request!", "error")

    if not file or not file.filename:
      flash("No file selected!", "error")
      return redirect(request.url)

    filepath = os.path.join(current_app.config["UPLOAD_DIR"], file.filename)
    file.save(filepath)

    # Get whether user made the upload private
    private = False
    if request.form.get('private', None) == "on":
      private = True 
  
    newPhoto = Photo(name = request.form['user'], 
                    caption = request.form['caption'],
                    description = request.form['description'],
                    file = file.filename,
                    private = private)
    db.session.add(newPhoto)
    if private:
      flash('New Photo at /uploads/%s' % newPhoto.file)
    else:
      flash('New Photo %s Successfully Created' % newPhoto.name)
    db.session.commit()
    return redirect(url_for('main.homepage'))
  else:
    return render_template('upload.html')

# This is called when clicking on Edit. Goes to the edit page.
@main.route('/photo/<int:photo_id>/edit/', methods = ['GET', 'POST'])
# If user not logged in they will be redirected to /login 
@login_required
def editPhoto(photo_id):

  editedPhoto = db.session.query(Photo).filter_by(id = photo_id).one()
  '''
  Check if the current user's username does not match the uploaded photo's username
  and the user is not an admin.
  If so, return to the home page with an error message
  '''
  if current_user.username != editedPhoto.name and not current_user.admin:
    flash("You are not authorised to edit this photo")
    return redirect(url_for('main.homepage'))

  if request.method == 'POST':
    if request.form['user']:
      editedPhoto.name = request.form['user']
      editedPhoto.caption = request.form['caption']
      editedPhoto.description = request.form['description']
      db.session.add(editedPhoto)
      db.session.commit()
      flash('Photo Successfully Edited %s' % editedPhoto.name)
      return redirect(url_for('main.homepage'))
  else:
    return render_template('edit.html', photo = editedPhoto)


# This is called when clicking on Delete. 
@main.route('/photo/<int:photo_id>/delete/', methods = ['GET','POST'])
# If user not logged in they will be redirected to /login 
@login_required
def deletePhoto(photo_id):
  photo = db.session.query(Photo).filter_by(id = photo_id).one()
  '''
  Check if the current user's username does not match the uploaded photo's username
  and the user is not an admin.
  If so, return to the home page with an error message
  '''
  if current_user.username != photo.name and not current_user.admin:
    flash("You are not authorised to delete this photo")
    return redirect(url_for('main.homepage'))

  fileResults = db.session.execute(text('select file from photo where id = ' + str(photo_id)))
  filename = fileResults.first()[0]
  filepath = os.path.join(current_app.config["UPLOAD_DIR"], filename)
  os.unlink(filepath)
  db.session.execute(text('delete from photo where id = ' + str(photo_id)))
  db.session.commit()
  
  flash('Photo id %s Successfully Deleted' % photo_id)
  return redirect(url_for('main.homepage'))

# This is called when a user clicks like on a photo
@main.route('/like/<int:photo_id>/', methods = ['GET','POST'])
# If user not logged in they will be redirected to /login 
@login_required
def likePhoto(photo_id):
  liked = db.session.query(Like).filter_by(photo_id = photo_id, user_id = current_user.id).first()
  if liked:
    db.session.delete(liked)
    db.session.commit()
    
  else:
    new_like = Like(photo_id=photo_id, user_id=current_user.id)
    db.session.add(new_like)
    db.session.commit()

  return redirect(url_for('main.homepage'))

