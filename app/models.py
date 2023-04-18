from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String(64), unique=True, index=True) 
    username = db.Column(db.String(64), unique=True, index=True) 
    password_hash = db.Column(db.String(128)) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

class Role(db.Model): 
    __tablename__ = 'roles' 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64), unique=True) 
    default = db.Column(db.Boolean, default=False, index=True) 
    permissions = db.Column(db.Integer) 
    users = db.relationship('User', backref='role', lazy='dynamic')