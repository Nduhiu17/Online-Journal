from app import app
from app.database import drop_entries_table, drop_users_table, create_users_table, create_entries_table
import unittest
import json

from config import TestingConfig


class RegistrationTestCase(unittest.TestCase):

    def tearDown(self):
        drop_entries_table()
        drop_users_table()
        create_users_table()
        create_entries_table

    def setUp(self):
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        self.app.testing = True

    def register_user(self, username="nduhiu", email="nduhiu2020@gmail.com", password="password"):
        user = {
            "username": username,
            "email": email,
            "password": password
        }
        return self.client.post('/api/v1/register/', data=json.dumps(user), content_type='application/json')


    def test_registration_with_empty_password_field(self):
        """This tests registering a user with missing password"""
        username = "nduhiu"
        email = "nduhiu2020@gmail.com"
        password = " "
        user = {
            "username": username,
            "email": email,
            "password": password
        }
        response = self.client.post('/api/v1/auth/signup', data=json.dumps(user),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    if __name__ == "__main__":
        unittest.main()
