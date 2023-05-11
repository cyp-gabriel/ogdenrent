from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, DateField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class NameForm(FlaskForm): 
   name = StringField('What is your name?', validators=[DataRequired()]) 
   submit = SubmitField('Submit')

class CustomerApplicationForm(FlaskForm):
   first_name = StringField('First name', validators=[DataRequired()])
   last_name = StringField('Last name', validators=[DataRequired()]) 
   dob = DateField('Date of Birth', validators=[DataRequired()])
   phone = StringField('Phone #', validators=[DataRequired()])
   ssn = StringField('SSN', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired()])

   num_pets = IntegerField('Number of pets')
   num_kids = IntegerField('Number of children')
   has_pets = BooleanField('Do you have pets?')
   
   prev_addr_street1 = StringField('Street #1')
   prev_addr_street2 = StringField('Street#2')
   prev_addr_city = StringField('City')
   prev_addr_state = StringField('State')
   prev_addr_zip = StringField('Zip')

   submit = SubmitField('Submit')