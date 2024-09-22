import unittest

from secure.headers import Server


class TestServerHeader(unittest.TestCase):
    def test_default_server(self):
        """Test default Server header value (NULL)."""
        server_header = Server()
        self.assertEqual(server_header.header_value, "")

    def test_set_custom_server(self):
        """Test setting a custom Server header value."""
        server_header = Server().set("CustomServer")
        self.assertEqual(server_header.header_value, "CustomServer")

    def test_clear_server(self):
        """Test clearing the Server header to default value (NULL)."""
        server_header = Server().set("CustomServer").clear()
        self.assertEqual(server_header.header_value, "")


if __name__ == "__main__":
    unittest.main()
