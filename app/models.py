from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from datetime import datetime
from . import db

class Permission: 
    FOLLOW = 1 
    COMMENT = 2 
    WRITE = 4 
    MODERATE = 8 
    ADMIN = 16

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String(64), unique=True, index=True) 
    username = db.Column(db.String(64), unique=True, index=True) 
    password_hash = db.Column(db.String(128)) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['OGDENRENT_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    
    def __repr__(self): 
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute, fiend.')
    
    @password.setter 
    def password(self, password): 
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password): 
        return check_password_hash(self.password_hash, password)
    
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

class Role(db.Model): 
    __tablename__ = 'roles' 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64), unique=True) 
    default = db.Column(db.Boolean, default=False, index=True) 
    permissions = db.Column(db.Integer) 
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
            
    def __repr__(self): 
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
            
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Owner': [Permission.WRITE, Permission.COMMENT, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        
        db.session.commit()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    phone = db.Column(db.String(64))
    ssn = db.Column(db.String(64))
    email = db.Column(db.String(64))

    num_pets = db.Column(db.Integer)
    num_kids = db.Column(db.Integer)
    has_pets = db.Column(db.Boolean)

    prev_addr_street1 = db.Column(db.String(64))
    prev_addr_street2 = db.Column(db.String(64))
    prev_addr_city = db.Column(db.String(64))
    prev_addr_state = db.Column(db.String(64))
    prev_addr_zip = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)