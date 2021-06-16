from flask import Blueprint, request, redirect, url_for, flash, g

bp = Blueprint("message", __name__, url_prefix="/message")

@bp.route("/send/<int:ticket_id>", methods=("POST",))
def send(ticket_id: int):
    """ open a ticket and redirect the client to another page """

    if request.method == "POST":
        user_id = 1
        message_text = request.form["message_text"]

        # TODO: check valid user

        ticket = g.ticket_model.get_ticket(ticket_id)

        if ticket.is_closed:
            # TODO: display error template 
            return redirect(url_for("ticket.discover"))

        g.message_model.send_message(ticket_id, user_id, message_text)

        flash(f"User {user_id} sent message to ticket with id: {ticket_id}")

        return redirect(url_for("ticket.view", ticket_id=ticket_id))

    # TODO: display error template 
    return redirect(url_for("ticket.discover"))
