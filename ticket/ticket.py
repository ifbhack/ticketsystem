from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from ticket.db import get_database
from ticket.models import TicketModel

bp = Blueprint("ticket", __name__, url_prefix="/ticket")

@bp.before_app_request
def create_ticket_model():
    """create_ticket_model and store it in a flask request context """

    db_conn = get_database()
    g.ticket_model = TicketModel(db_conn)

@bp.route("/open", methods=("GET", "POST"))
def open():
    """ open a ticket and redirect the client to another page """

    if request.method == "POST":
        user_id = 1
        title = request.form["title"]
        description = request.form["description"]
        tag = request.form["tag"]

        # TODO: check valid user

        ticket = g.ticket_model.open_ticket(user_id, title, description, tag)

        flash(f"Created ticket with ticket id: {ticket.ticket_id}")

        return redirect(url_for("ticket.view", ticket_id=ticket.ticket_id))

    return render_template("ticket/open.html")

@bp.route("/discover", methods=("GET",))
def discover():
    """ discover all of the tickets ever created """

    # TODO: add filter options
    tickets = g.ticket_model.get_tickets()
    return render_template("ticket/discover.html", tickets=tickets)

@bp.route("/<int:ticket_id>", methods=("GET",))
def view(ticket_id: int):
    """ view a single ticket """

    ticket = g.ticket_model.get_ticket(ticket_id)

    return render_template("ticket/view.html", ticket=ticket)

@bp.route("/close/<int:ticket_id>", methods=("POST",))
def close(ticket_id: int):
    """ close a ticket """

    g.ticket_model.close_ticket(ticket_id)

    flash(f"Closed ticket with ticket id: {ticket_id}")

    return redirect(url_for("ticket.view", ticket_id=ticket_id))
