from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import Ticket

tickets_blueprint = Blueprint('tickets', __name__)


class CreateTicketAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            ticket = Ticket(
                name=post_data.get('name'),
                email=post_data.get('email'),
                subject=post_data.get('subject'),
                type=post_data.get('type'),
                urgency=post_data.get('urgency'),
                message=post_data.get('message'),
            )
            # insert the ticket
            db.session.add(ticket)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Ticket successfully added!'
            }
            return make_response(jsonify(responseObject)), 201
        except Exception:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401


# define the API resources
creation_ticket_view = CreateTicketAPI.as_view('create_ticket_api')


# add Rules for API Endpoints
tickets_blueprint.add_url_rule(
    '/tickets/create',
    view_func=creation_ticket_view,
    methods=['POST']
)
