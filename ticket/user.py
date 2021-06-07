class User:
    user_id = 0
    guild_id = 0
    username = None
    is_assignable = False

    def __init__(self, user_id, guild_id, username, is_assignable = False):
        self.user_id = user_id
        self.guild_id = guild_id
        self.username = username
        self.is_assignable = is_assignable

class UserModel:
    _db_conn = None

    def __init__(self, db_conn):
        self._db_conn = db_conn

    def create_user(self, guild_id, username, is_assignable = False):
        pass

    def create_message(self, user, ticket, message_title, message_text):
        pass
