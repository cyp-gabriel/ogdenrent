import re
import unittest
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign up' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # register a new account
        response = self.client.post('/auth/register', data={
            'email': 'boone.cabal@gmail.com',
            'username': 'admin',
            'password': 'bogh',
            'password2': 'bogh'
        })
        self.assertEqual(response.status_code, 302)

        # login with the new account
        response = self.client.post('/auth/login', data={
            'email': 'boone.cabal@gmail.com',
            'password': 'bogh'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have not confirmed your account yet' in response.get_data(as_text=True))

        # send a confirmation token
        user = User.query.filter_by(email='boone.cabal@gmail.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        # log out
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))

    def test_email(self):
        from flask_mail import Message
        from app import mail

        try:
            
            msg = Message('test email', sender='contact@boonecabal.co', recipients=['cabalscorner@gmail.com'])
            msg.body = 'This is the plain text body'
            msg.html = 'This is the <b>HTML</b> body'
            with self.app.app_context():
                mail.send(msg),

        except Exception as e:
            print(str(e))
