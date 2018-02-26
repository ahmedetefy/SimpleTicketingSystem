import time
import json
import unittest

from project.server import db
from project.server.models import Ticket
from project.tests.base import BaseTestCase


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
