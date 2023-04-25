from datetime import datetime 
from flask import render_template, session, redirect, url_for 
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
   return render_template('Dashboard.html')

@main.route('/new_application', methods=['GET', 'POST'])
def new_application():
   form = CustomerApplicationForm()
   if form.validate_on_submit():
      customer = Customer(
         first_name=form.first_name.data,
         last_name=form.last_name.data,
         dob=form.dob.data,
         phone=form.phone.data,
         ssn=form.ssn.data,
         email=form.email.data)
      db.session.add(customer)
      db.session.commit()

      return redirect(url_for('.index'))

   return render_template('new_application.html', form=form)

@main.route('/new_client_application', methods=['GET', 'POST'])
def new_client_application():
   form = CustomerApplicationForm()
   if form.validate_on_submit():
      customer = Customer(
         first_name=form.first_name.data,
         last_name=form.last_name.data,
         dob=form.dob.data,
         phone=form.phone.data,
         ssn=form.ssn.data,
         email=form.email.data)
      db.session.add(customer)
      db.session.commit()

      return redirect(url_for('.index'))

   return render_template('new_client_applicaton.html', form=form)