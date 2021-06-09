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
        # life saver: https://ongspxm.gitlab.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(ValueError):
            self._message_model.send_message(0, 1, self._test_message)
        with self.assertRaises(ValueError):
            self._message_model.send_message(1, 0, self._test_message)
        with self.assertRaises(ValueError):
            self._message_model.send_message(1, 1, "")

        test_message = self.__send_test_message()

        message = self._message_model.get_message(test_message.message_id)
        self.assertEqual(message.message_text, self._test_message)

    def test_get_message(self):
        self.__send_test_message()
        msg = self._message_model.get_message(1)
        self.assertEqual(msg.message_id, 1)

        with self.assertRaises(ValueError):
            self._message_model.get_message(0)

        with self.assertRaises(message.MessageNotFoundError):
            self._message_model.get_message(3479284732)



    def __check_messages_subset(self, test_messages, messages):
        message_ids = []
        for message in messages:
            message_ids.append(message.message_id)

        self.assertTrue(set(test_messages).issubset(message_ids))

    def test_get_ticket_messages(self):
        test_messages = [
            self.__send_test_message().message_id,
            self.__send_test_message().message_id,
            self.__send_test_message().message_id,
        ]

        with self.assertRaises(ValueError):
            self._message_model.get_ticket_messages(0)

        with self.assertRaises(message.MessageNotFoundError):
            self._message_model.get_ticket_messages(24324325)

        self.__check_messages_subset(test_messages,
                                     self._message_model.get_ticket_messages(1, 4))

        self.__check_messages_subset(test_messages,
                                     self._message_model.get_ticket_messages(1, offset=1))

        self.__check_messages_subset(test_messages,
                                     self._message_model.get_ticket_messages(1))

    @classmethod
    def tearDownClass(cls):
        cls._db_conn.close()
