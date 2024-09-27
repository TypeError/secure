import unittest

from secure.headers import CustomHeader


class TestCustomHeader(unittest.TestCase):
    def test_custom_header_initialization(self):
        """Test initialization of a custom header with name and value."""
        custom_header = CustomHeader("X-Custom-Header", "custom-value")
        self.assertEqual(custom_header.header_name, "X-Custom-Header")
        self.assertEqual(custom_header.header_value, "custom-value")

    def test_set_custom_header_value(self):
        """Test setting a new value for the custom header."""
        custom_header = CustomHeader("X-Custom-Header", "initial-value")
        custom_header.set("updated-value")
        self.assertEqual(custom_header.header_value, "updated-value")

    def test_method_chaining(self):
        """Test method chaining while setting a new value for the custom header."""
        custom_header = CustomHeader("X-Custom-Header", "initial-value").set(
            "new-value"
        )
        self.assertEqual(custom_header.header_value, "new-value")


if __name__ == "__main__":
    unittest.main()
