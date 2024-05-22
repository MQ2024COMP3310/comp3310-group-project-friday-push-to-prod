from . import db
from flask_login import UserMixin

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    file = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(600), nullable=True)
    private =  db.Column(db.Boolean(False))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'           : self.id,
           'name'         : self.name,
           'caption'      : self.caption,
           'file'         : self.file,
           'desc'         : self.description,
           'private'    : self.private
       }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin =  db.Column(db.Boolean(False))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'id'    : self.id,
            'username'        : self.username,
            'password'    : self.password,
            'admin' : self.admin
       }
 
 
