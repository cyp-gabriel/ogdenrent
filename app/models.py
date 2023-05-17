from werkzeug.security import	generate_password_hash,	check_password_hash
from itsdangerous.url_safe import	URLSafeTimedSerializer as	Serializer
from flask_login import	UserMixin, AnonymousUserMixin
import jwt

from flask_login import	UserMixin
from flask import	current_app, url_for
from datetime	import datetime, timezone, timedelta
from . import	db

from . import	login_manager

class	AnonymousUser(AnonymousUserMixin):
	def	can(self,	permissions):
		return False

	def	is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def	load_user(user_id):
	return User.query.get(int(user_id))

class	Permission:	
	FOLLOW = 1 
	COMMENT	=	2	
	WRITE	=	4	
	MODERATE = 8 
	ADMIN	=	16

class	User(UserMixin,	db.Model):
	__tablename__	=	'users'	
	id = db.Column(db.Integer, primary_key = True) 
	email	=	db.Column(db.String(64), unique=True,	index=True)	
	username = db.Column(db.String(64),	unique=True, index=True) 
	password_hash	=	db.Column(db.String(128))	
	role_id	=	db.Column(db.Integer,	db.ForeignKey('roles.id'))

	confirmed	=	db.Column(db.Boolean,	default=False)

	def	__init__(self, **kwargs):
		super(User,	self).__init__(**kwargs)
		if self.role is	None:
			if self.email	== current_app.config['OGDENRENT_ADMIN']:
				self.role	=	Role.query.filter_by(name='Administrator').first()
			if self.role is	None:
				self.role	=	Role.query.filter_by(default=True).first()
	
	def	__repr__(self):	
		return '<User	%r>' % self.username

	@property
	def	password(self):
		raise	AttributeError('password is	not	a	readable attribute,	fiend.')
	
	@password.setter 
	def	password(self, password):	
		self.password_hash = generate_password_hash(password)

	def	verify_password(self,	password): 
		return check_password_hash(self.password_hash, password)
	
	def	can(self,	perm):
		return self.role is	not	None and self.role.has_permission(perm)
	
	def	is_administrator(self):
		return self.can(Permission.ADMIN)

	def	generate_auth_token(self,	expiration):
		s	=	Serializer(current_app.config['SECRET_KEY'],
									 expires_in=expiration)
		return s.dumps({'id':	self.id}).decode('utf-8')

	@staticmethod
	def	verify_auth_token(token):
		s	=	Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.query.get(data['id'])

	def	to_json(self):
		json_user	=	{
			'username':	self.username,
			'email': self.email
		}
		return json_user

	def	generate_confirmation_token(self,	expiration=3600):
		now	=	datetime.now(timezone.utc)
		later	=	now	+	timedelta(seconds=expiration)
		timestamp	=	later.timestamp()
		token	=	jwt.encode(
			{
				"exp": timestamp,
				"confirm": self.id
			},
			current_app.config['SECRET_KEY'],
			algorithm="HS256"
		)

		return token

	def	confirm(self,	token):
		try:
			data = jwt.decode(
				token,
				current_app.config['SECRET_KEY'],
				leeway=10,
				algorithms=["HS256"]
			)
		except:
			return False
		if data.get('confirm') !=	self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def	generate_reset_token(self, expiration=3600):
		s	=	Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id}).decode('utf-8')

	@staticmethod
	def	reset_password(token,	new_password):
		s	=	Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		user = User.query.get(data.get('reset'))
		if user	is None:
			return False
		user.password	=	new_password
		db.session.add(user)
		return True

	def	generate_email_change_token(self,	new_email, expiration=3600):
		s	=	Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'change_email':	self.id, 'new_email':	new_email}).decode('utf-8')

	def	change_email(self, token):
		s	=	Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('change_email')	!= self.id:
			return False
		new_email	=	data.get('new_email')
		if new_email is	None:
			return False
		if self.query.filter_by(email=new_email).first() is	not	None:
			return False
		self.email = new_email
		self.avatar_hash = self.gravatar_hash()
		db.session.add(self)
		return True

class	Role(db.Model):	
	__tablename__	=	'roles'	
	id = db.Column(db.Integer, primary_key=True) 
	name = db.Column(db.String(64),	unique=True) 
	default	=	db.Column(db.Boolean,	default=False, index=True) 
	permissions	=	db.Column(db.Integer)	
	users	=	db.relationship('User',	backref='role',	lazy='dynamic')

	def	__init__(self, **kwargs):
		super(Role,	self).__init__(**kwargs)
		if self.permissions	is None:
			self.permissions = 0
				
	def	__repr__(self):	
		return '<Role	%r>' % self.name

	def	has_permission(self, perm):
		return self.permissions	&	perm ==	perm

	def	add_permission(self, perm):
		if not self.has_permission(perm):
			self.permissions +=	perm
				
	def	remove_permission(self,	perm):
		if self.has_permission(perm):
			self.permissions -=	perm

	def	reset_permissions(self):
		self.permissions = 0

	@staticmethod
	def	insert_roles():
				roles	=	{
						'User':	[Permission.FOLLOW,	Permission.COMMENT,	Permission.WRITE],
						'Owner': [Permission.WRITE,	Permission.COMMENT,	Permission.MODERATE],
						'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,	Permission.ADMIN],
				}
				default_role = 'User'

				for	r	in roles:
						role = Role.query.filter_by(name=r).first()

						if role	is None:
								role = Role(name=r)
						role.reset_permissions()
						for	perm in	roles[r]:
								role.add_permission(perm)
						role.default = (role.name	== default_role)
						db.session.add(role)
				
				db.session.commit()

class	Customer(db.Model):
	__tablename__	=	'customers'
	id = db.Column(db.Integer, primary_key=True)

	first_name = db.Column(db.String(64))
	last_name	=	db.Column(db.String(64))
	dob	=	db.Column(db.DateTime, index=True, default=datetime.utcnow)
	phone	=	db.Column(db.String(64))
	ssn	=	db.Column(db.String(64))
	email	=	db.Column(db.String(64))
	driver_license = db.Column(db.String(64))
	state_id = db.Column(db.String(64))

	num_adults = db.Column(db.Integer)
	num_kids = db.Column(db.Integer)
	has_pets = db.Column(db.Boolean)

	prev_addr_street1	=	db.Column(db.String(64))
	prev_addr_street2	=	db.Column(db.String(64))
	prev_addr_city = db.Column(db.String(64))
	prev_addr_state	=	db.Column(db.String(64))
	prev_addr_zip	=	db.Column(db.String(64))

	contact_to_verify_last_addr	=	db.Column(db.String(64))
	contact_to_verify_last_phone = db.Column(db.String(64))
	current_employer = db.Column(db.String(64))
	position = db.Column(db.String(64))
	emp_contact_name = db.Column(db.String(64))
	emp_contact_phone	=	db.Column(db.String(64))
	
	time_on_job	=	db.Column(db.Integer)
	monthly_net_income = db.Column(db.Float)
	paydays	=	db.Column(db.Integer)
	
	receiving_ssi	=	db.Column(db.Boolean)
	monthly_ssi_amount = db.Column(db.Float)
	
	best_hours = db.Column(db.String(64))
	between_x_AM = db.Column(db.Integer)
	between_y_PM = db.Column(db.Integer)

	has_service_animal = db.Column(db.Boolean)
	former_military	=	db.Column(db.Boolean)
	is_felon = db.Column(db.Boolean)
	is_on_registry = db.Column(db.Boolean)
	po_name	=	db.Column(db.String(64))
	po_phone = db.Column(db.String(64))
	offender_number	=	db.Column(db.String(64))
	
	auto_make	=	db.Column(db.String(64))
	auto_model = db.Column(db.String(64))
	auto_color = db.Column(db.String(64))
	auto_plate = db.Column(db.String(64))

	emergency_contact_name = db.Column(db.String(64))
	emergency_contact_phone	=	db.Column(db.String(64))
	
	rented_here_before = db.Column(db.Boolean)
	rented_here_at_addr	=	db.Column(db.String(64))

	signature	=	db.Column(db.String(64))
	date_signed	=	db.Column(db.DateTime, default=datetime.utcnow)

	def	__init__(self, **kwargs):
		super(Customer,	self).__init__(**kwargs)

	def	to_json(self):
		json_customer	=	{
			'first_name':	self.first_name,
			'last_name': self.last_name,
			'dob': self.dob,
			'phone': self.phone,
			'ssn': self.ssn,
			'email': self.email,
			'driver_license':	self.driver_license,
			'state_id':	self.state_id,
			'num_adults':	self.num_adults,
			'num_kids':	self.num_kids,
			'has_pets':	self.has_pets,
			'prev_addr_street1': self.prev_addr_street1,
			'prev_addr_street2': self.prev_addr_street2,
			'prev_addr_city':	self.prev_addr_city,
			'prev_addr_state': self.prev_addr_state,
			'prev_addr_zip': self.prev_addr_zip,
			'contact_to_verify_last_addr': self.contact_to_verify_last_addr,
			'contact_to_verify_last_phone':	self.contact_to_verify_last_phone,
			'current_employer':	self.current_employer,
			'position':	self.position,
			'emp_contact_name':	self.emp_contact_name,
			'emp_contact_phone': self.emp_contact_phone,
			'time_on_job': self.time_on_job,
			'monthly_net_income':	self.monthly_net_income,
			'paydays': self.paydays,
			'receiving_ssi': self.receiving_ssi,
			'monthly_ssi_amount':	self.monthly_ssi_amount,
			'best_hours':	self.best_hours,
			'between_x_AM':	self.between_x_AM,
			'between_y_PM':	self.between_y_PM,
			'has_service_animal':	self.has_service_animal,
			'former_military': self.former_military,
			'is_felon':	self.is_felon,
			'is_on_registry':	self.is_on_registry,
			'po_name': self.po_name,
			'po_phone':	self.po_phone,
			'offender_number': self.offender_number,
			'auto_make': self.auto_make,
			'auto_model':	self.auto_model,
			'auto_color':	self.auto_color,
			'auto_plate':	self.auto_plate,
			'emergency_contact_name':	self.emergency_contact_name,
			'emergency_contact_phone': self.emergency_contact_phone,
			'rented_here_before':	self.rented_here_before,
			'rented_here_at_addr': self.rented_here_at_addr,
			'signature': self.signature,
			'date_signed': self.date_signed
		}
		return json_customer

