import sqlite3
from . import user
from typing import List

# TODO: when we have a couple more errors, put in seperate file
class UserAssignViolationError(Exception):
    pass

class Ticket:
    ticket_id = 0
    user_id = 0
    title = None
    description = None
    is_closed = False
    tag = None
    assigned_user = None
    created_on = None

    def __init__(self, ticket_id: int, user_id: int, title: str,
                 description: str, created_on: str,
                 assigned_user = None, tag = None):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.assigned_user = assigned_user
        self.tag = tag
        self.created_on = created_on

class TicketModel:
    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def open_ticket(self, user: user.User, title: str, description: str, tag: str = None):
        self._db_conn.execute("""
            INSERT INTO
                ticket (user_id, ticket_title, ticket_description, ticket_tag)
            VALUES (?, ?, ?, ?)
        """, (user.user_id, title, description, tag))
        self._db_conn.commit()

    def get_ticket(self, ticket_id) -> Ticket:
        cursor = self._db_conn.cursor()
        cursor.execute("""
            SELECT
                *
            FROM ticket
            WHERE ticket_id = ?
        """, (ticket_id,))
        row = cursor.fetchone()

        return Ticket(row[0]. row[1], row[3], row[4], row[7], row[2], row[6], row[5])

    def get_tickets(self, limit: int, offset: int = 0) -> List[Ticket]:
        cursor = self._db_conn.cursor()
        cursor.execute("""
            SELECT
                *
            FROM ticket
            LIMIT ? ORDER BY ?
        """, (limit, offset))
        return cursor.fetchall()


    def assign_user(self, ticket: Ticket, user: user.User):
        if user.user_id == ticket.user_id:
            # log error
            raise UserAssignViolationError("cannot assign a ticket to the same ticket owner")

        self._db_conn.execute("""
            UPDATE ticket
                SET assigned_user_id = ?
            WHERE
                ticket_id = ?
            LIMIT 1
        """, (user.user_id, ticket.ticket_id))
        self._db_conn.commit()

    def add_tag(self, ticket: Ticket, tag: str):
        self._db_conn.execute("""
            UPDATE ticket
                SET ticket_tag = ?
            WHERE
                ticket_id = ?
            LIMIT 1
        """, (tag, ticket.ticket_id))
        self._db_conn.commit()

    def close_ticket(self, ticket: Ticket):
        self._db_conn.execute("""
            UPDATE ticket
                SET is_closed  = 1
            WHERE
                ticket_id = ?
            LIMIT 1
        """, (ticket.ticket_id,))
        self._db_conn.commit()
