from datetime import datetime 
from flask import render_template, session, redirect, url_for 
from . import main 
from .forms import NameForm, CustomerApplicationForm
from .. import db 
from ..models import User

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
      # ...
      return redirect(url_for('.new_application'))

   return render_template('Client-Application.html', form=form)