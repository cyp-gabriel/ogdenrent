from flask_wtf import FlaskForm 
#from flask_table import LinkCol
from wtforms import StringField, SubmitField, DateField
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
   #edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
   submit = SubmitField('Submit')