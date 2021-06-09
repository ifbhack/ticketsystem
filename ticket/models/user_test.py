import unittest
from ticket import db
from ticket.models import user

class TestMessageModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._db_conn = db.get_test_database()

    def setUp(self):
        self._user_model: user.UserModel = user.UserModel(self._db_conn)

    def __create_test_user(self) -> user.User:
         return self._user_model.create_user("123456789012345678", "joshturge", True)

    def test_create_user(self):
        user = self.__create_test_user()
        queried_user = self._user_model.get_user(user.user_id)
        self.assertEqual(user.user_id, queried_user.user_id)

        with self.assertRaises(ValueError):
            self._user_model.create_user("12345678", "joshturge", True)

    def test_get_user(self):
        usr = self.__create_test_user()
        queried_user = self._user_model.get_user(usr.user_id)
        self.assertEqual(usr.user_id, queried_user.user_id)

        with self.assertRaises(ValueError):
            self._user_model.get_user(0)

        with self.assertRaises(user.NoUserFoundError):
            self._user_model.get_user(9438759357394)

    @classmethod
    def tearDownClass(cls):
        cls._db_conn.close()
