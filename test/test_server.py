import unittest
from Calendar import socket_server as s


class positive_test(unittest.TestCase):

    def test_positive_date(self):
        self.assertEqual(s.check_day(6, 6), True)

    def test_positive_date_string(self):
        self.assertEqual(s.check_day("6", 6), True)

    def test_positive_check_date(self):
        self.assertEqual(s.check_date("06/06"), True)


class negative_test(unittest.TestCase):

    def test_negative_date(self):
        self.assertEqual(s.check_day(40, 6), False)

    def test_negative_date_string(self):
        self.assertEqual(s.check_day("test", 6), False)
        self.assertEqual(s.check_day(10, "test2"), False)

    def test_negative_check_date_day(self):
        self.assertEqual(s.check_date("06/"), False)

    def test_negative_check_date_month(self):
        self.assertEqual(s.check_date("/06"), False)

    def test_negative_check_date_too_high(self):
        self.assertEqual(s.check_date("06/90"), False)
        self.assertEqual(s.check_date("90/6"), False)

    def test_negative_check_date_invalid(self):
        self.assertEqual(s.check_date("0606"), False)


class TestMonth(unittest.TestCase):

    def setUp(self):
        self.testCalendar = s.Month()
        self.testCalendar.struct_calendar()
        self.testActivity = s.Activity("06/06", "test_title", "test_description")
        self.user = s.Client("test_addr")
        self.user.set_username("Test")
        self.testActivity.user = self.user

    def test_get_activities(self):
        self.testCalendar.add_activity(self.testActivity)
        returnedData = self.testCalendar.get_activities("6", "6")
        self.assertIn("test_title", returnedData)

    def test_get_activities_negative(self):
        self.testCalendar.add_activity(self.testActivity)
        returnedData = self.testCalendar.get_activities("5", "6")
        self.assertIn("No meetings on that day", returnedData)

    def test_add_activity(self):
        self.testCalendar.add_activity(self.testActivity)
        self.assertIn('6', self.testCalendar.user_meetings)

    def test_add_activity_multiple(self):
        testActivity = s.Activity("06/06", "another_test_title", "another_test_description")
        testActivity.user = self.user
        self.testCalendar.add_activity(testActivity)
        self.assertIn('6', self.testCalendar.user_meetings['6'])

    def test_add_activity_different_date(self):
        testActivity = s.Activity("06/07", "another_test_title", "another_test_description")
        testActivity.user = self.user
        self.testCalendar.add_activity(testActivity)
        self.assertIn('7', self.testCalendar.user_meetings['6'])

    def test_fetch_month_string(self):
        self.assertEqual(self.testCalendar.fetch_month("june"), 5)

    def test_negative_fetch_month_string(self):
        self.assertEqual(self.testCalendar.fetch_month("thisisnotadate"), False)

    def test_fetch_month_int(self):
        self.assertEqual(self.testCalendar.fetch_month("6"), 5)

    def test_negative_fetch_month_int(self):
        self.assertEqual(self.testCalendar.fetch_month("60"), False)

    def test_add_calendar_activity(self):
        self.testCalendar.add_calendar_activity("06/06")
        self.assertEqual(self.testCalendar.calendar_page[5][6], "X")


if __name__ == '__main__':
    unittest.main()
