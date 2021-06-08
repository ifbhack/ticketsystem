import sqlite3
from typing import List, Any

class Message:
    """Message contains fields related to a ticket message"""
    message_id: int = 0
    ticket_id: int = 0
    user_id: int = 0
    message_text: str = ""
    message_sent_on: str = ""

    def __init__(self, message_id: int, ticket_id: int, user_id: int,
                 message_text: str, message_sent_on: str = ""):
        self.message_id = message_id
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.message_text = message_text
        self.message_sent_on = message_sent_on

class MessageModel:
    """MessageModel allows a caller to send and get messages for a ticket"""
    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def __convert_row_message(self, row: List[Any]) -> Message:
        return Message(row[0], row[1], row[2], row[3], row[4])

    def send_message(self, ticket_id: int, user_id: int, message_text: str) -> Message:
        """send_message to a ticket from a specified user."""

        cursor = self._db_conn.cursor()
        # TODO: figure out how to return the current timestamp from sqlite
        cursor.execute("""
            INSERT INTO
                message (ticket_id, user_id, message_text)
            VALUES (?, ?, ?)
        """, (ticket_id, user_id, message_text))

        return Message(cursor.lastrowid, ticket_id, user_id, message_text)

    def get_message(self, message_id: int) -> Message:
        """
        get_message with specified message_id
        this method is exported for unit testing
        """

        cursor = self._db_conn.cursor()

        cursor.execute("""
            SELECT * FROM message WHERE message_id = ?
        """, (message_id,))

        row = cursor.fetchone()

        return self.__convert_row_message(row)

    def get_ticket_messages(self, ticket_id: int, limit: int = 0,
                            offset: int = 0) -> List[Message]:
        """
        get_ticket_messages from a specified ticket
        optional limit and offset provided, send all messages by default.
        """
        cursor = self._db_conn.cursor()

        sqlquery = "SELECT * FROM message WHERE ticket_id = ?"

        if limit != 0:
            sqlquery += " LIMIT " + str(limit)

        if offset != 0:
            sqlquery += " ORDER BY " + str(offset)

        cursor.execute(sqlquery, (ticket_id,))

        messages: List[Message] = []
        rows = cursor.fetchall()
        for row in rows:
            messages.append(self.__convert_row_message(row))

        return messages
