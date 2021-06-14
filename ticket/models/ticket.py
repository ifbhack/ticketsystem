import sqlite3
from typing import List, Iterable, Any
from ticket.models.user import User

# TODO: when we have a couple more errors, put in seperate file
class UserAssignViolationError(Exception):
    pass

class TicketNotFoundError(Exception):
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
    # TODO: add sqlite error handling and additional checks for things like closed tickets or non-assignable users.
    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def open_ticket(self, user_id: int, title: str, description: str, tag: str = "") -> Ticket:
        """open_ticket for a specified user. A ticket is open by default and the datetime is
        automatically set within the database.

        returns a ticket with the given data and ticket id.
        """

        if user_id == 0:
            raise ValueError(f"user_id is invalid: got {user_id}")
        if title == "" or description == "":
            raise ValueError(f"""title or description is an empty string: title:
                             ({title}) description: ({description})""")

        cursor = self._db_conn.cursor()

        # NOTE(joshturge): Since I'm running sqlite 3.34.* I don't have access to the
        # RETURNING functionality, and will need to make a seperate query to the database.
        #
        # TODO: in the future utilise RETURNING (https://www.sqlite.org/lang_returning.html)
        # to return the creation date of the ticket.
        cursor.execute("""
            INSERT INTO
                ticket (user_id, ticket_title, ticket_description, ticket_tag, is_closed)
            VALUES (?, ?, ?, ?, 0)
        """, (user_id, title, description, tag))

        self._db_conn.commit()

        # get the ticket_created_on datetime
        cursor.execute("""
            SELECT
                ticket_created_on
            FROM ticket
            WHERE ticket_id = ?
        """, (cursor.lastrowid,))

        created_on = cursor.fetchone()

        return Ticket(cursor.lastrowid, user_id, title, description, created_on=created_on,
                      is_closed=False, tag=tag)

    def __convert_ticket_row(self, row: List[Any]) -> Ticket:
        return Ticket(row[0], row[1], row[3], row[4], row[7], row[6], row[5], row[2])

    def get_ticket(self, ticket_id: int) -> Ticket:
        """get_ticket with a given ticket_id. If no ticket is found, a TicketNotFoundError
        exception will be raised"""

        if ticket_id == 0:
            raise ValueError(f"ticket_id is invalid: got {ticket_id}")

        cursor = self._db_conn.cursor()
        cursor.execute("""
            SELECT
                *
            FROM ticket
            WHERE ticket_id = ?
        """, (ticket_id,))

        row = cursor.fetchone()
        if row == None:
            raise TicketNotFoundError(f"ticket with ticket_id: {ticket_id} not found")

        return self.__convert_ticket_row(row)

    def __get_tickets(self, sqlquery: str, parameters: Iterable[Any], limit: int = 0, offset: int = 0) -> List[Ticket]:
        """get_tickets from the database, given an sqlquery. Sets the limit and offset automatically.
        All tickets returned by default with no offset

        returns an iterable list of tickets or a TicketNotFoundError when no tickets are found.
        """
        if limit != 0:
            sqlquery += " LIMIT " + str(limit)

        if offset != 0:
            sqlquery += " ORDER BY " + str(offset)

        cursor = self._db_conn.cursor()
        cursor.execute(sqlquery, parameters)

        tickets: List[Ticket] = []
        rows = cursor.fetchall()

        if len(rows) == 0:
            raise TicketNotFoundError("no tickets were found")

        for row in rows:
            tickets.append(self.__convert_ticket_row(row))

        return tickets

    def get_tickets(self, limit: int = 0, offset: int = 0) -> List[Ticket]:
        """get_tickets from the database
        All tickets returned by default with no offset

        returns an iterable list of tickets or a TicketNotFoundError when no tickets are found.
        """

        return self.__get_tickets("SELECT * FROM ticket", (), limit, offset)

    def get_tickets_by_user(self, user_id: int, limit: int = 0, offset: int = 0) -> List[Ticket]:
        """get_tickets_by_user from the database given a user_id. 
        All tickets returned by default with no offset

        returns an iterable list of tickets or a TicketNotFoundError when no tickets are found.
        """

        if user_id == 0:
            raise ValueError(f"invalid user_id: got {user_id}")

        return self.__get_tickets("SELECT * FROM ticket WHERE user_id = ?", (user_id,), limit, offset)

    def assign_user(self, ticket: Ticket, user: User):
        """assign_user to a specified ticket"""

        if ticket.ticket_id == 0:
            raise ValueError(f"ticket.ticket_id is invalid: got {ticket.ticket_id}")
        elif user.user_id == 0:
            raise ValueError(f"user_id is invalid: got {user.user_id}")

        if user.user_id == ticket.user_id:
            raise UserAssignViolationError("cannot assign a ticket to the same ticket owner")
        elif not user.is_assignable:
            raise UserAssignViolationError("cannot assign a ticket to a non-assignable user")

        # TODO: raise an exception when the user is not assignable to tickets
        self._db_conn.execute("""
            UPDATE ticket
                SET assigned_user_id = ?
            WHERE
                ticket_id = ?
        """, (user.user_id, ticket.ticket_id))

        self._db_conn.commit()

        ticket.assigned_user_id = user.user_id

    def add_tag(self, ticket: Ticket, tag: str):
        """add_tag or replace tag for a given ticket"""
        if ticket.ticket_id == 0:
            raise ValueError(f"ticket.ticket_id is invalid: got {ticket.ticket_id}")

        if tag == "":
            raise ValueError(f"tag is invalid: got empty string")

        self._db_conn.execute("""
            UPDATE ticket
                SET ticket_tag = ?
            WHERE
                ticket_id = ?
        """, (tag, ticket.ticket_id))
        self._db_conn.commit()

        ticket.tag = tag

    def close_ticket(self, ticket: Ticket):
        """close_ticket given a valid ticket to close"""
        if ticket.ticket_id == 0:
            raise ValueError(f"ticket.ticket_id is invalid: got {ticket.ticket_id}")

        self._db_conn.execute("""
            UPDATE ticket
                SET is_closed  = 1
            WHERE
                ticket_id = ?
        """, (ticket.ticket_id,))
        self._db_conn.commit()

        ticket.is_closed = True
