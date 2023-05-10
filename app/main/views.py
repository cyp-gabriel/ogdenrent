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
   return render_template('dashboard.html', customers=customers)

@main.route('/new_application', methods=['GET', 'POST'])
def new_application():
   form = CustomerApplicationForm()

   if form.validate_on_submit():

      # clear database if Clear checkbox is selected
      if request.form.get('clear') != None:
         db.session.query(Customer).delete()
         db.session.commit()

      # add new customer to database
      customer = Customer(
         first_name=form.first_name.data,
         last_name=form.last_name.data,
         dob=form.dob.data,
         phone=form.phone.data,
         ssn=form.ssn.data,
         email=form.email.data)
      db.session.add(customer)
      db.session.commit()

      flash('Thanks for submitting your name, fiend.  Now leave, please.')

      return redirect(url_for('main.index'))

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