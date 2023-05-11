from datetime import datetime 
from flask import render_template, session, redirect, url_for, flash, request
from . import main 
from .forms import NameForm, CustomerApplicationForm
from .. import db 
from ..models import User, Customer

@main.route('/', methods=['GET', 'POST']) 
def index():
   form = NameForm() 
   if form.validate_on_submit():
      # ...
      return redirect(url_for('.index'))

   return render_template('index.html')

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
   customers = Customer.query.all()
   form = CustomerApplicationForm()
   return render_template('dashboard.html', form=form, customers=customers)

@main.route('/new_application', methods=['GET', 'POST'])
def new_application():
   form = CustomerApplicationForm()
   form.ssn.data = '522-21-6667'

   if form.validate_on_submit():

      # clear database if Clear checkbox is selected
      if request.form.get('clear') != None:
         db.session.query(Customer).delete()
         db.session.commit()

      # add new customer to database
      c = Customer()
      c.first_name = form.first_name.data
      c.last_name = form.last_name.data
      c.dob = form.dob.data
      c.phone = form.phone.data
      c.ssn = form.ssn.data
      c.email = form.email.data

      # num_pets = form.num_pets
      # num_kids = form.num_kids
      # has_pets = form.has_pets
      c.num_pets = 0
      c.num_kids = 0
      c.has_pets = False

      c.prev_addr_street1 = form.prev_addr_street1.data
      c.prev_addr_street2 = form.prev_addr_street2.data
      c.prev_addr_city = form.prev_addr_city.data
      c.prev_addr_state = form.prev_addr_state.data
      c.prev_addr_zip = form.prev_addr_zip.data


      db.session.add(c)
      db.session.commit()

      flash('Thanks for submitting your name, fiend.  Now leave, please.')

      # return redirect(url_for('main.index'))

   return render_template('new_application.html', form=form)

@main.route('/customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
   c = Customer.query.filter(Customer.id == customer_id).first()
   
   if c:
      form = CustomerApplicationForm(formdata=request.form, obj=c)

      if request.method == 'GET':
         form.first_name.data = c.first_name
         form.last_name.data = c.last_name
         form.dob.data = c.dob
         form.phone.data = c.phone
         form.ssn.data = c.ssn
         form.email.data = c.email

         form.num_pets = c.form.num_pets 
         form.num_kids = c.form.num_kids 
         form.has_pets = c.form.has_pets 

         form.prev_addr_street1 = c.form.prev_addr_street1 
         form.prev_addr_street2 = c.form.prev_addr_street2 
         form.prev_addr_city = c.form.prev_addr_city 
         form.prev_addr_state = c.form.prev_addr_state 
         form.prev_addr_zip = c.form.prev_addr_zip 

      elif request.method == 'POST' and form.validate():
         save_changes(c, form)
         flash('Customer update, fiend.  Now leave, please.')

      return render_template('edit_customer.html', form=form)
   
   else:
      return 'Error loading #{customer_id}'.format(customer_id=customer_id)

def save_changes(c, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    c.first_name = form.first_name.data
    c.last_name = form.last_name.data
    c.dob = form.dob.data
    c.phone = form.phone.data
    c.ssn = form.ssn.data
    c.email = form.email.data

    if new:
        # Add the new c to the database
        db.session.add(c)

    # commit the data to the database
    db.session.commit()