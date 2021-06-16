from flask import Blueprint, render_template, request, redirect, url_for, flash, g

bp = Blueprint("ticket", __name__, url_prefix="/ticket")

@bp.route("/open", methods=("GET", "POST"))
def open():
    """ open a ticket and redirect the client to another page """

    if request.method == "POST":
        user_id = 1
        title = request.form["title"]
        description = request.form["description"]

        tag = request.form["tag"]
        if tag == "":
            tag = "Issue"

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

    messages = g.message_model.get_ticket_messages(ticket_id)

    return render_template("ticket/view.html", ticket=ticket, messages=messages)

@bp.route("/close/<int:ticket_id>", methods=("POST",))
def close(ticket_id: int):
    """ close a ticket """

    g.ticket_model.close_ticket(ticket_id)

    flash(f"Closed ticket with ticket id: {ticket_id}")

    return redirect(url_for("ticket.view", ticket_id=ticket_id))
