import sqlite3
from typing import List, Any

# TODO: when we have a couple more errors, put in seperate file
class UserAssignViolationError(Exception):
    pass

class Ticket:
    ticket_id: int= 0
    user_id: int = 0
    title: str = ""
    description: str = ""
    is_closed: bool = False
    tag: str = ""
    assigned_user_id: int = 0
    created_on: str = ""

    def __init__(self, ticket_id: int, user_id: int, title: str,
                 description: str, created_on: str,
                 is_closed: bool,
                 tag: str = "", assigned_user_id: int = 0):

        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.assigned_user_id = assigned_user_id
        self.tag = tag
        self.is_closed = is_closed
        self.created_on = created_on

class TicketModel:
    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def open_ticket(self, user_id: int, title: str, description: str, tag: str = "") -> Ticket:
        cursor = self._db_conn.cursor()

        # TODO: figure out how to return the 'ticket_created_on' field without creating
        # another query. For now the returned ticket will have "" for attr 'created_on'.
        cursor.execute("""
            INSERT INTO
                ticket (user_id, ticket_title, ticket_description, ticket_tag, is_closed)
            VALUES (?, ?, ?, ?, 0)
        """, (user_id, title, description, tag))

        return Ticket(cursor.lastrowid, user_id, title, description, created_on="",
                      is_closed=False, tag=tag)

    def __convert_ticket_row(self, row: List[Any]) -> Ticket:
        return Ticket(row[0], row[1], row[3], row[4], row[7], row[6], row[5], row[2])

    def get_ticket(self, ticket_id: int) -> Ticket:
        cursor = self._db_conn.cursor()
        cursor.execute("""
            SELECT
                *
            FROM ticket
            WHERE ticket_id = ?
        """, (ticket_id,))
        row = cursor.fetchone()

        return self.__convert_ticket_row(row)

    def get_tickets(self, limit: int = 0, offset: int = 0) -> List[Ticket]:

        sqlquery = "SELECT * FROM ticket"

        if limit != 0:
            sqlquery += " LIMIT " + str(limit)

        if offset != 0:
            sqlquery += " ORDER BY " + str(offset)

        cursor = self._db_conn.cursor()
        cursor.execute(sqlquery)

        tickets: List[Ticket] = []
        rows = cursor.fetchall()
        for row in rows:
            tickets.append(self.__convert_ticket_row(row))

        return tickets

    def assign_user(self, ticket: Ticket, user_id: int):
        if user_id == ticket.user_id:
            # log error
            raise UserAssignViolationError("cannot assign a ticket to the same ticket owner")

        self._db_conn.execute("""
            UPDATE ticket
                SET assigned_user_id = ?
            WHERE
                ticket_id = ?
        """, (user_id, ticket.ticket_id))
        self._db_conn.commit()

        ticket.assigned_user_id = user_id


    def add_tag(self, ticket: Ticket, tag: str):
        self._db_conn.execute("""
            UPDATE ticket
                SET ticket_tag = ?
            WHERE
                ticket_id = ?
        """, (tag, ticket.ticket_id))
        self._db_conn.commit()

        ticket.tag = tag

    def close_ticket(self, ticket: Ticket):
        self._db_conn.execute("""
            UPDATE ticket
                SET is_closed  = 1
            WHERE
                ticket_id = ?
        """, (ticket.ticket_id,))
        self._db_conn.commit()

        ticket.is_closed = True
