import json

from project.server import db
from project.server.models import BlacklistToken
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


def create_ticket(self, email, name, subject, type, urgency, message):
    return self.client.post(
        '/tickets/create',
        data=json.dumps(dict(
            email=email,
            name=name,
            subject=subject,
            type=type,
            urgency=urgency,
            message=message
        )),
        content_type='application/json',
    )


def ticket_list(self, resp_register):
    return self.client.get(
        '/tickets/list',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                resp_register.data.decode()
            )['auth_token']
        )
    )


class TestTicketCreation(BaseTestCase):

    def test_ticket_creation_full_information(self):
        """ Test for ticket creation registration """
        with self.client:
            response = create_ticket(self, "byrd@byrd.com", "byrd",
                                     "Hello World", "Bug Report",
                                     "High", "Testing")
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
        """ Test for obtaining ticket list when user is not logged in """
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
            response = ticket_list(self, resp_register)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')

    def test_ticket_list_logged_in(self):
        """ Test for obtaining ticket list when user is logged in """
        with self.client:
            # Add dummy tickets
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
            create_ticket(self, "byrd@byrd.com", "byrd2", "Hello World",
                          "Bug Report", "High", "Testing")
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
            response = ticket_list(self, resp_login)
            data = json.loads(response.data.decode())
            self.assertTrue(data[0]['name'] == 'byrd')
            self.assertTrue(data[1]['name'] == 'byrd2')


class TestTicketUpdateAPI(BaseTestCase):
    def test_ticket_update_not_logged_in(self):
        """ Test for ticket update when user is not logged in """
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
            # Ticket Update Request
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
        """ Test for ticket update when user is logged in """
        with self.client:
            # Add dummy tickets
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
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
            #  Request ticket update
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


class TestTicketDeleteAPI(BaseTestCase):
    def test_ticket_delete_not_logged_in(self):
        """ Test for ticket deletion when user is not logged in """
        with self.client:
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
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
            # Delete Ticket Request
            response = self.client.delete(
                '/tickets/delete/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')

    def test_ticket_delete_logged_in(self):
        """ Test for ticket deletion when user is logged in """
        with self.client:
            # Add dummy tickets
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
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
            #  Request delete ticket
            response = self.client.delete(
                '/tickets/delete/1',
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Ticket successfully deleted!')


class TestAddCommentTicketAPI(BaseTestCase):
    def test_comment_ticket_add_not_logged_in(self):
        """ Test for creation of a comment when user is not logged in """
        with self.client:
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
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
            # create comment request
            response = self.client.post(
                '/tickets/1/createComment',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')

    def test_comment_ticket_add_logged_in(self):
        """ Test for creation of a comment when user is logged in """
        with self.client:
            # Add dummy tickets
            create_ticket(self, "byrd@byrd.com", "byrd", "Hello World",
                          "Bug Report", "High", "Testing")
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
            # create comment request
            response = self.client.post(
                '/tickets/1/createComment',
                content_type='application/json',
                data=json.dumps(dict(
                    email="byrd@byrd.com",
                    comment=" Commenting ")),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Comment successfully added!')
