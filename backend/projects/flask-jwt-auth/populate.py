from project.server import db

from project.server.models import User, Ticket, Comment


def registerUser():
    user = User(email="byrd@byrd.com",
                password="byrd")
    db.session.add(user)
    db.session.commit()


def populateTickets():
    ticket = Ticket(name="John Appleseed",
                    type="Bug Report",
                    urgency="Medium Urgency",
                    subject="Urgent Request",
                    email="john@appleseed.com",
                    message=("Lorem Ipsum is simply" +
                             "dummy text of the printing and typesetting" +
                             "industry. Lorem Ipsum has been the industry's" +
                             "standard dummy text ever since the 1500s, " +
                             "when an unknown printer took a galley of " +
                             "type and scrambled it to make a " +
                             "type specimen book."))
    comment1 = Comment(email="byrd@byrd.com",
                       comment="This issue needs to be fixed ASAP")
    comment2 = Comment(email="employee@byrd.com",
                       comment="Will be fixed in 24 hours")
    ticket.ticketComments = [comment1, comment2]

    ticket2 = Ticket(name="Petra Byrd",
                     type="Feature Request",
                     urgency="Low Urgency",
                     subject="Can you do that?",
                     email="petra@byrd.com",
                     message=("Lorem Ipsum is simply" +
                              "dummy text of the printing and typesetting" +
                              "industry. Lorem Ipsum has been the industry's" +
                              "standard dummy text ever since the 1500s, " +
                              "when an unknown printer took a galley of " +
                              "type and scrambled it to make a " +
                              "type specimen book."))
    comment3 = Comment(email="manager@byrd.com",
                       comment="This issue will not be handled")
    ticket2.ticketComments = [comment3]
    db.session.add(ticket)
    db.session.add(ticket2)
    db.session.commit()


if __name__ == '__main__':
    registerUser()
    populateTickets()
