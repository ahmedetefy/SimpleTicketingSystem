from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import Ticket, User

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


class ListTicketAPI(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                tickets = Ticket.query.all()
                ticketlist = []
                for ticket in tickets:
                    tempTicket = {
                        "name": ticket.name,
                        "email": ticket.email,
                        "subject": ticket.subject,
                        "type": ticket.type,
                        "urgency": ticket.urgency,
                        "message": ticket.message
                    }
                    ticketlist.append(tempTicket)
                return make_response(jsonify(ticketlist)), 201
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


# define the API resources
creation_ticket_view = CreateTicketAPI.as_view('create_ticket_api')
list_ticket_view = ListTicketAPI.as_view('list_ticket_api')


# add Rules for API Endpoints
tickets_blueprint.add_url_rule(
    '/tickets/create',
    view_func=creation_ticket_view,
    methods=['POST']
)
tickets_blueprint.add_url_rule(
    '/tickets/list',
    view_func=list_ticket_view,
    methods=['GET']
)
