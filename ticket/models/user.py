import sqlite3

GUILD_ID_LENGTH = 18

class NoUserFoundError(Exception):
    pass

class User:
    """contains fields related to a user"""
    user_id: int = 0
    guild_id: str = ""
    username: str = ""
    is_assignable: bool = False

    def __init__(self, user_id: int, guild_id: str, username: str, is_assignable: bool = False):
        self.user_id = user_id
        self.guild_id = guild_id
        self.username = username
        self.is_assignable = is_assignable

class UserModel:
    """allows a caller to create or retrieve a user"""

    _db_conn: sqlite3.Connection

    def __init__(self, db_conn: sqlite3.Connection):
        self._db_conn = db_conn

    def create_user(self, guild_id: str, username: str, is_assignable = False) -> User:
        """
        create_user from guild_id and with username. Can also specify if they
        are assignable to tickets, false by default
        """

        if len(guild_id) != GUILD_ID_LENGTH:
            raise ValueError(f"guild_id is of invalid length: wanted {GUILD_ID_LENGTH}: got {len(guild_id)}")

        cursor = self._db_conn.cursor()
        cursor.execute("""
            INSERT INTO
                user (guild_id, user_name, is_assignable)
            VALUES(?, ?, ?)
        """, (guild_id, username, is_assignable))

        self._db_conn.commit()

        return User(cursor.lastrowid, guild_id, username, is_assignable)

    def get_user(self, user_id: int) -> User:
        """get_user with specified user_id"""

        if user_id == 0:
            raise ValueError(f"user_id is invalid: got {user_id}")

        cursor = self._db_conn.cursor()
        cursor.execute("""
            SELECT * FROM user WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        if row == None:
            raise NoUserFoundError("user not found")

        return User(int(row[0]), row[1], row[2], bool(row[3]))
