import unittest
from Calendar import client as c


class positive_tests(unittest.TestCase):
    def test_client(self):
        client = c.Client()
        self.assertEqual(client.ADDR, ("127.0.0.1", 8080))


if __name__ == '__main__':
    unittest.main()
