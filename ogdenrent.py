import os
from dotenv	import load_dotenv

dotenv_path	=	os.path.join(os.path.dirname(__file__),	'.env')
if os.path.exists(dotenv_path):
		load_dotenv(dotenv_path)

COV	=	None
if os.environ.get('FLASK_COVERAGE'):
		import coverage
		COV	=	coverage.coverage(branch=True, include='app/*')
		COV.start()

import sys
import click
from app import	create_app,	db 
from app.models	import User, Role, Customer, Permission
from flask_migrate import	Migrate, upgrade

app	=	create_app(os.getenv('FLASK_CONFIG') or	'default') 
migrate	=	Migrate(app, db)

@app.shell_context_processor 
def	make_shell_context():	
	return dict(db=db, User=User,	Role=Role, Permission=Permission,	Customer=Customer)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@app.cli.command()
def	deploy():
    """Run deployment	tasks."""
    #	migrate	database to	latest revision
    #upgrade()
    db.create_all()
    db.session.commit()

    #	create or	update user	roles
    Role.insert_roles()

    # insert admin user
    admin_role = Role.query.filter_by(name='Administrator').first()
    admin = User(
        email='contact@boonecabal.co', 
        username='admin', 
        password='Bogh0428$',
        role_id=admin_role.id,
        confirmed=True)
    admin.role_id = admin_role.id

    db.session.add(admin)
    db.session.commit()

    from datetime import datetime
    ted = Customer()
    ted.first_name = 'Ted'
    ted.last_name = 'Bell'
    ted.dob = datetime.now()
    ted.email = 'ted@bell.com'
    ted.driver_license = '12345'
    ted.phone = '555-555-5555'
    ted.signature = 'Ted'
    ted.date_signed = datetime.now()
    ted.emergency_contact_name = 'Mai'
    ted.emergency_contact_phone = '555-555-5555'
    ted.contact_to_verify_last_addr = 'Rhomboid'
    ted.contact_to_verify_last_phone = '555-555-5555'
    
    db.session.add(ted)
    db.session.commit()