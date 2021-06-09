import unittest
from ticket import db
from ticket.models import ticket, user

class TestTicketModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_user: user.User = user.User(1, "123456789012345678", "joshturge", True)
        cls._db_conn = db.get_test_database()

        cls._db_conn.execute("""
            INSERT INTO
                user (guild_id, user_name, is_assignable)
            VALUES (?, ?, ?)
        """, (cls._test_user.guild_id, cls._test_user.username, cls._test_user.is_assignable))
        cls._db_conn.commit()

    def setUp(self):
        self._ticket_model: ticket.TicketModel = ticket.TicketModel(self._db_conn)

    def __open_test_ticket(self) -> ticket.Ticket:
        return self._ticket_model.open_ticket(self._test_user.user_id,
                                       "Test Ticket",
                                       "This is a test ticket",
                                       "TestTicket")

    def test_open_ticket(self):
        ticket = self.__open_test_ticket()
        self.assertNotEqual(ticket.ticket_id, 0)

    def test_get_ticket(self):
        test_ticket = self.__open_test_ticket()
        ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)
        self.assertNotEqual(ticket.ticket_id, 0)
        self.assertEqual(ticket.ticket_id, test_ticket.ticket_id)

    def test_get_tickets(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        tickets = self._ticket_model.get_tickets()

        ticket_ids = []
        for ticket in tickets:
            ticket_ids.append(ticket.ticket_id)

        self.assertTrue(set(test_tickets).issubset(ticket_ids))

    def test_assign_user(self):
        test_user = user.User(2, "12", "james", True)
        test_ticket = self._ticket_model.open_ticket(test_user.user_id,
                                       "Test Ticket",
                                       "This is a test ticket",
                                       "TestTicket")

        self._ticket_model.assign_user(test_ticket, self._test_user.user_id)

        self.assertEqual(test_ticket.assigned_user_id, self._test_user.user_id)

        # query the ticket again just to make sure it was committed to the db
        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertEqual(queried_test_ticket.assigned_user_id, self._test_user.user_id)

    def test_add_tag(self):

        test_tag = "thisTag"

        test_ticket = self.__open_test_ticket()
        self._ticket_model.add_tag(test_ticket, test_tag)

        self.assertEqual(test_ticket.tag, test_tag)

        # query the ticket again just to make sure it was committed to the db
        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertEqual(queried_test_ticket.tag, test_tag)

    def test_close_ticket(self):
        test_ticket = self.__open_test_ticket()
        self._ticket_model.close_ticket(test_ticket)

        self.assertTrue(test_ticket.is_closed)

        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertTrue(queried_test_ticket.is_closed)


    @classmethod
    def tearDownClass(cls):
        cls._db_conn.close()

if __name__ == '__main__':
    unittest.main()
