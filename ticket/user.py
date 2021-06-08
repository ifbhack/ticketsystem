import sqlite3
from . import ticket

class User:
    user_id = 0
    guild_id = None
    username = None
    is_assignable = False

    def __init__(self, user_id: int, guild_id: str, username: str, is_assignable = False):
        self.user_id = user_id
        self.guild_id = guild_id
        self.username = username
        self.is_assignable = is_assignable

class UserModel:
    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def create_user(self, guild_id: str, username: str, is_assignable = False):
        self._db_conn.execute("""
            INSERT INTO
                user (guild_id, user_name, is_assignable)
            VALUES(?, ?, ?)
        """, (guild_id, username, is_assignable))
        self._db_conn.commit()

    def create_message(self, user: User, ticket: ticket.Ticket, message_text: str):
        self._db_conn.execute("""
            INSERT INTO
                message (ticket_id, user_id, message_text)
            VALUES (?, ?, ?)
        """, (ticket.ticket_id, user.user_id, message_text))
        self._db_conn.commit()
