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

        # TODO: change to the index page
        return redirect(url_for("ticket.view"))

    return render_template("ticket/open.html")

@bp.route("/view", methods=("GET",))
def view():
    """ view all of the tickets ever created """

    # TODO: add filter options
    tickets = g.ticket_model.get_tickets()
    return render_template("ticket/view.html", tickets=tickets)
