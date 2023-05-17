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

        response = self.client.delete(
            '/api/v1/delete_customer/{}'.format(ted.id),
            headers=self.get_api_headers('john@example.com', 'cat'))
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('has been deleted', json_response['success'])

    def test_no_auth(self):
        response = self.client.get('/api/v1/users/3',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

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
