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
   driver_license = StringField("Driver's License")
   state_id = StringField('State ID', validators=[DataRequired()])

   num_adults = IntegerField('Number of adults living w/you')
   num_kids = IntegerField('Children')
   num_pets = IntegerField('Pets')
   
   prev_addr_street1 = StringField('Street #1')
   prev_addr_street2 = StringField('Street#2')
   prev_addr_city = StringField('City')
   prev_addr_state = StringField('State')
   prev_addr_zip = StringField('Zip')

   contact_to_verify_last_addr	= StringField('contact_to_verify_last_addr')
   contact_to_verify_last_phone = StringField('contact_to_verify_last_phone')
   current_employer = StringField('current_employer')
   position = StringField('position')
   emp_contact_name = StringField('emp_contact_name')
   emp_contact_phone	= StringField('emp_contact_phone')
	
   time_on_job	= StringField('time_on_job')
   monthly_net_income = StringField('monthly_net_income')
   paydays	= StringField('paydays')
	
   receiving_ssi	= StringField('receiving_ssi')
   monthly_ssi_amount = StringField('monthly_ssi_amount')
	
   best_hours = StringField('best_hours')
   between_x_AM = StringField('between_x_AM')
   between_y_PM = StringField('between_y_PM')

   has_service_animal = StringField('has_service_animal')
   former_military	= StringField('former_military')
   is_felon = StringField('is_felon')
   is_on_registry = StringField('is_on_registry')
   po_name	= StringField('po_name')
   po_phone = StringField('po_phone')
   offender_number	= StringField('offender_number')
	
   auto_make	= StringField('auto_make')
   auto_model = StringField('auto_model')
   auto_color = StringField('auto_color')
   auto_plate = StringField('auto_plate')

   emergency_contact_name = StringField('emergency_contact_name')
   emergency_contact_phone	= StringField('emergency_contact_phone')
	
   rented_here_before = StringField('rented_here_before')
   rented_here_at_addr	= StringField('rented_here_at_addr')

   signature	= StringField('signature')
   date_signed	= StringField('date_signed')

   photo = StringField('Photo')

   submit = SubmitField('Submit')
