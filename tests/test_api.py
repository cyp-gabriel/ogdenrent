import unittest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role, Customer

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def test_customers(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u1 = User(email='john@example.com', username='john',
                  password='cat', confirmed=True, role=r)

        db.session.add(u1)
        db.session.commit()
        
        ted = Customer()
        ted.first_name = 'Ted'
        ted.last_name = 'Bell'
        from datetime import datetime
        ted.dob = datetime.utcnow()
        ted.phone = '555-555-5555'
        ted.ssn = '123-45-6789'
        ted.email = 'ted@example.com'

        # num_pets = form.num_pets
        # num_kids = form.num_kids
        # has_pets = form.has_pets
        ted.num_pets = 0
        ted.num_kids = 0
        ted.has_pets = False

        ted.prev_addr_street1 = '123 Main St'
        ted.prev_addr_street2 = 'Apt 1'
        ted.prev_addr_city = 'New York'
        ted.prev_addr_state = 'NY'
        ted.prev_addr_zip = '10001'

        db.session.add(ted)
        db.session.commit()

        response = self.client.put(
            '/api/v1/active_customer/{}'.format(ted.id),
            headers=self.get_api_headers('john@example.com', 'cat'))

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertGreater(json_response['active_customer_id'], 0)

        response = self.client.get(
            '/api/v1/active_customer',
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertGreater(json_response['active_customer_id'], 0)

    # def test_404(self):
    #     response = self.client.get(
    #         '/wrong/url',
    #         headers=self.get_api_headers('email', 'password'))
    #     self.assertEqual(response.status_code, 404)
    #     json_response = json.loads(response.get_data(as_text=True))
    #     self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get('/api/v1/users/3',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

    # def test_bad_auth(self):
    #     # add a user
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u = User(email='john@example.com', password='cat', confirmed=True,
    #              role=r)
    #     db.session.add(u)
    #     db.session.commit()

    #     # authenticate with bad password
    #     response = self.client.get(
    #         '/api/v1/posts/',
    #         headers=self.get_api_headers('john@example.com', 'dog'))
    #     self.assertEqual(response.status_code, 401)

    # def test_token_auth(self):
    #     # add a user
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u = User(email='john@example.com', password='cat', confirmed=True,
    #              role=r)
    #     db.session.add(u)
    #     db.session.commit()

    #     # issue a request with a bad token
    #     response = self.client.get(
    #         '/api/v1/posts/',
    #         headers=self.get_api_headers('bad-token', ''))
    #     self.assertEqual(response.status_code, 401)

    #     # get a token
    #     response = self.client.post(
    #         '/api/v1/tokens/',
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertEqual(response.status_code, 200)
    #     json_response = json.loads(response.get_data(as_text=True))
    #     self.assertIsNotNone(json_response.get('token'))
    #     token = json_response['token']

    #     # issue a request with the token
    #     response = self.client.get(
    #         '/api/v1/posts/',
    #         headers=self.get_api_headers(token, ''))
    #     self.assertEqual(response.status_code, 200)

    # def test_anonymous(self):
    #     response = self.client.get(
    #         '/api/v1/posts/',
    #         headers=self.get_api_headers('', ''))
    #     self.assertEqual(response.status_code, 401)

    # def test_unconfirmed_account(self):
    #     # add an unconfirmed user
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u = User(email='john@example.com', password='cat', confirmed=False,
    #              role=r)
    #     db.session.add(u)
    #     db.session.commit()

    #     # get list of posts with the unconfirmed account
    #     response = self.client.get(
    #         '/api/v1/posts/',
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertEqual(response.status_code, 403)

    def test_users(self):
        # add two users
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u1 = User(email='john@example.com', username='john',
                  password='cat', confirmed=True, role=r)
        u2 = User(email='susan@example.com', username='susan',
                  password='dog', confirmed=True, role=r)
        db.session.add_all([u1, u2])
        db.session.commit()

        # get users
        response = self.client.get(
            '/api/v1/users/{}'.format(u1.id),
            headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'john')
        response = self.client.get(
            '/api/v1/users/{}'.format(u2.id),
            headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'susan')
