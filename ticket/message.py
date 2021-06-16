from flask import Blueprint, request, redirect, url_for, flash, g

from ticket.db import get_database
from ticket.models import MessageModel
from ticket.models import TicketModel

bp = Blueprint("message", __name__, url_prefix="/message")

@bp.before_app_request
def create_message_model():
    """create_message_model and store it in a flask request context """

    db_conn = get_database()
    g.message_model = MessageModel(db_conn)

@bp.route("/send/<int:ticket_id>", methods=("POST",))
def send(ticket_id: int):
    """ open a ticket and redirect the client to another page """

    if request.method == "POST":
        user_id = 1
        message_text = request.form["message_text"]

        # TODO: check valid user

        db_conn = get_database()
        g.ticket_model = TicketModel(db_conn)
        ticket = g.ticket_model.get_ticket(ticket_id)

        if ticket.is_closed:
            # TODO: display error template 
            return redirect(url_for("ticket.discover"))

        g.message_model.send_message(ticket_id, user_id, message_text)

        flash(f"User {user_id} sent message to ticket with id: {ticket_id}")

        return redirect(url_for("ticket.view", ticket_id=ticket_id))

    # TODO: display error template 
    return redirect(url_for("ticket.discover"))
