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
                        "id": ticket.id,
                        "name": ticket.name,
                        "email": ticket.email,
                        "subject": ticket.subject,
                        "type": ticket.type,
                        "urgency": ticket.urgency,
                        "message": ticket.message,
                        "status": ticket.status
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


class UpdateTicketAPI(MethodView):
    def put(self):
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
                post_data = request.get_json()
                ticket = Ticket.query.filter_by(
                    id=post_data.get('id')).first()
                ticket.name = post_data.get('name')
                ticket.email = post_data.get('email')
                ticket.subject = post_data.get('subject')
                ticket.type = post_data.get('type')
                ticket.urgency = post_data.get('urgency')
                ticket.message = post_data.get('message')
                ticket.status = post_data.get('status')
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Ticket successfully updated!'
                }
                return make_response(jsonify(responseObject)), 201
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


class DeleteTicketAPI(MethodView):
    def delete(self, ticketID):
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
                Ticket.query.filter_by(id=ticketID).delete()
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Ticket successfully deleted!'
                }
                return make_response(jsonify(responseObject)), 201
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
edit_ticket_view = UpdateTicketAPI.as_view('edit_ticket_api')
delete_ticket_view = DeleteTicketAPI.as_view('delete_ticket_api')


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
tickets_blueprint.add_url_rule(
    '/tickets/edit',
    view_func=edit_ticket_view,
    methods=['PUT']
)
tickets_blueprint.add_url_rule(
    '/tickets/delete/<int:ticketID>',
    view_func=delete_ticket_view,
    methods=['DELETE']
)
