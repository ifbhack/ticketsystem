class Ticket:
    ticket_id = 0
    user_id = 0
    title = None
    description = None
    is_closed = False
    tag = None
    assigned_user = None
    created_on = None

    def __init__(self, user_id, ticket_id, title, description, created_on, assigned_user = None, tag = None):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.assigned_user = assigned_user
        self.tag = tag
        self.created_on = created_on

class TicketModel:
    _db_conn = None

    def __init__(self, db_conn):
        self._db_conn = db_conn

    def open_ticket(self, user, title, description, tag = None):
        pass

    def assign_user(self, ticket, user):
        if user.user_id == ticket.user_id:
            # log error
            return None
        pass

    def add_tag(self, ticket, tag):
        pass

    def add_message(self, ticket, message):
        pass

    def close_ticket(self, ticket):
        pass
