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
        with self.assertRaises(ValueError):
            self._ticket_model.open_ticket(0,
                                       "Test Ticket",
                                       "This is a test ticket",
                                       "TestTicket")

        with self.assertRaises(ValueError):
            self._ticket_model.open_ticket(self._test_user.user_id,
                                       "",
                                       "This is a test ticket",
                                       "TestTicket")

        ticket = self.__open_test_ticket()
        self.assertNotEqual(ticket.ticket_id, 0)
        self.assertNotEqual(ticket.created_on, "")

    def test_get_ticket(self):

        with self.assertRaises(ValueError):
            self._ticket_model.get_ticket(0)

        with self.assertRaises(ticket.TicketNotFoundError):
            self._ticket_model.get_ticket(39837459375)

        test_ticket = self.__open_test_ticket()
        tkt = self._ticket_model.get_ticket(test_ticket.ticket_id)
        self.assertNotEqual(tkt.ticket_id, 0)
        self.assertEqual(tkt.ticket_id, test_ticket.ticket_id)

    def __check_ticket_subset(self, test_tickets, tickets):
        ticket_ids = []
        for ticket in tickets:
            ticket_ids.append(ticket.ticket_id)

        self.assertTrue(set(test_tickets).issubset(ticket_ids))

    def test_get_tickets(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets())
        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets(limit=10))
        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets(offset=1))

    def test_get_tickets_by_user(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets_by_user(self._test_user.user_id))

        with self.assertRaises(ValueError):
            self._ticket_model.get_tickets_by_user(0)

        with self.assertRaises(ticket.TicketNotFoundError):
            self._ticket_model.get_tickets_by_user(372947932)

    def test_get_tickets_by_title(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets_by_title("Test"))

        with self.assertRaises(ticket.TicketNotFoundError):
            self._ticket_model.get_tickets_by_title("no")

    def test_get_tickets_by_tag(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets_by_tag("Test"))

        with self.assertRaises(ticket.TicketNotFoundError):
            self._ticket_model.get_tickets_by_tag("no")

    def test_get_tickets_by_status(self):
        test_tickets = [
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
                self.__open_test_ticket().ticket_id,
            ]

        self.__check_ticket_subset(test_tickets, self._ticket_model.get_tickets_by_status(False))

    def test_assign_user(self):
        test_user = user.User(2, "12", "james", True)

        invalid_ticket = ticket.Ticket(0, test_user.user_id, "b", "d", "dw", False)

        with self.assertRaises(ValueError):
            self._ticket_model.assign_user(invalid_ticket, test_user)

        test_ticket = self._ticket_model.open_ticket(test_user.user_id,
                                       "Test Ticket",
                                       "This is a test ticket",
                                       "TestTicket")

        invalid_user = user.User(0, "123456789012345678", "b", False)

        with self.assertRaises(ValueError):
            self._ticket_model.assign_user(test_ticket, invalid_user)

        with self.assertRaises(ticket.UserAssignViolationError):
            self._ticket_model.assign_user(test_ticket, test_user)

        with self.assertRaises(ticket.UserAssignViolationError):
            invalid_user.user_id = 1
            self._ticket_model.assign_user(test_ticket, invalid_user)


        self._ticket_model.assign_user(test_ticket, self._test_user)

        self.assertEqual(test_ticket.assigned_user_id, self._test_user.user_id)

        # query the ticket again just to make sure it was committed to the db
        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertEqual(queried_test_ticket.assigned_user_id, self._test_user.user_id)

    def test_add_tag(self):

        test_tag = "thisTag"

        test_ticket = self.__open_test_ticket()
        self._ticket_model.add_tag(test_ticket, test_tag)

        invalid_ticket = ticket.Ticket(0, 1, "b", "d", "dw", False)

        with self.assertRaises(ValueError):
            self._ticket_model.add_tag(invalid_ticket, "ert")

        with self.assertRaises(ValueError):
            self._ticket_model.add_tag(test_ticket, "")

        self.assertEqual(test_ticket.tag, test_tag)

        # query the ticket again just to make sure it was committed to the db
        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertEqual(queried_test_ticket.tag, test_tag)

    def test_close_ticket(self):
        test_ticket = self.__open_test_ticket()
        self._ticket_model.close_ticket(test_ticket.ticket_id)

        queried_test_ticket = self._ticket_model.get_ticket(test_ticket.ticket_id)

        self.assertTrue(queried_test_ticket.is_closed)

        invalid_ticket = ticket.Ticket(0, 1, "b", "d", "dw", False)

        with self.assertRaises(ValueError):
            self._ticket_model.close_ticket(invalid_ticket.ticket_id)

    @classmethod
    def tearDownClass(cls):
        cls._db_conn.close()

if __name__ == '__main__':
    unittest.main()
