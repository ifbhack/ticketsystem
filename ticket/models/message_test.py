import unittest
from ticket import db
from ticket.models import message

class TestMessageModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._db_conn = db.get_test_database()

    def setUp(self):
        self._message_model: message.MessageModel = message.MessageModel(self._db_conn)
        self._test_message: str = "Test message"

    def __send_test_message(self) -> message.Message:
        return self._message_model.send_message(1, 1, self._test_message)

    def test_send_message(self):
        test_message = self.__send_test_message()
        message = self._message_model.get_message(test_message.message_id)
        self.assertEqual(message.message_text, self._test_message)

    def test_get_ticket_messages(self):
        test_messages = [
            self.__send_test_message().message_id,
            self.__send_test_message().message_id,
            self.__send_test_message().message_id,
        ]

        messages = self._message_model.get_ticket_messages(1)

        message_ids = []
        for message in messages:
            message_ids.append(message.message_id)

        self.assertTrue(set(test_messages).issubset(message_ids))

    @classmethod
    def tearDownClass(cls):
        cls._db_conn.close()
