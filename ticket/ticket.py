from flask import Blueprint

# EXAMPLE ticket model init:
# ==========================
#
#from ticket.db import get_database
#from .models.ticket import TicketModel
#
#db_conn = get_database()
#ticket_model = TicketModel(db_conn)

bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@bp.route('/open', methods=('GET', 'POST'))
def open_ticket():

    # ticket_model can then be used in the routes like:
    # ticket_model.open_ticket(<params>)

    return "open ticket"
