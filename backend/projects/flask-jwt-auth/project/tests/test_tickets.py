import time
import json
import unittest

from project.server import db
from project.server.models import Ticket, BlacklistToken
from project.tests.base import BaseTestCase


def register_user(self, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestTicketCreation(BaseTestCase):

    def test_ticket_creation_full_information(self):
        """ Test for ticket creation registration """
        with self.client:
            response = self.client.post(
                '/tickets/create',
                data=json.dumps(dict(
                    email="byrd@byrd.com",
                    name="byrd",
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing"
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Ticket successfully added!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_ticket_creation_missing_information(self):
        """ Test for ticket creation registration """
        with self.client:
            response = self.client.post(
                '/tickets/create',
                data=json.dumps(dict(
                    name="byrd",
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing"
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Some error occurred. Please try again.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)


class TestTicketListAPI(BaseTestCase):
    def test_ticket_list_not_logged_in(self):
        with self.client:
            # user registration
            resp_register = register_user(self, 'byrd@byrd.com', 'byrd')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/tickets/list',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')

    def test_ticket_list_logged_in(self):
        with self.client:
            # Add dummy tickets
            self.client.post(
                '/tickets/create',
                data=json.dumps(dict(
                    name="byrd",
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing",
                    email="byrd@byrd.com"
                )),
                content_type='application/json',
            )
            self.client.post(
                '/tickets/create',
                data=json.dumps(dict(
                    name="byrd2",
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing",
                    email="byrd@byrd.com"
                )),
                content_type='application/json',
            )
            # user registration
            resp_register = register_user(self, 'byrd@byrd.com', 'byrd')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = login_user(self, 'byrd@byrd.com', 'byrd')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            #  Request ticket list
            response = self.client.get(
                '/tickets/list',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data[0]['name'] == 'byrd')
            self.assertTrue(data[1]['name'] == 'byrd2')


class TestTicketUpdateAPI(BaseTestCase):
    def test_ticket_update_not_logged_in(self):
        with self.client:
            # user registration
            resp_register = register_user(self, 'byrd@byrd.com', 'byrd')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.put(
                '/tickets/edit',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')

    def test_ticket_update_logged_in(self):
        with self.client:
            # Add dummy tickets
            self.client.post(
                '/tickets/create',
                data=json.dumps(dict(
                    name="byrd",
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing",
                    email="byrd@byrd.com"
                )),
                content_type='application/json',
            )
            # user registration
            resp_register = register_user(self, 'byrd@byrd.com', 'byrd')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = login_user(self, 'byrd@byrd.com', 'byrd')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            #  Request ticket list
            response = self.client.put(
                '/tickets/edit',
                data=json.dumps(dict(
                    name="byrd2y",
                    id=1,
                    subject="Hello World",
                    type="Bug Report",
                    urgency="High",
                    message="Testing",
                    email="byrd@byrd.com",
                    status="open")),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Ticket successfully updated!')
