import unittest

from secure import Secure
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
        custom_header = CustomHeader("X-Custom-Header", "initial-value").set("new-value")
        self.assertEqual(custom_header.header_value, "new-value")

    def test_constructor_rejects_carriage_return(self):
        with self.assertRaisesRegex(ValueError, "custom header value must not contain CR/LF characters"):
            CustomHeader("X-Custom-Header", "safe\runsafe")

    def test_constructor_rejects_line_feed(self):
        with self.assertRaisesRegex(ValueError, "custom header value must not contain CR/LF characters"):
            CustomHeader("X-Custom-Header", "safe\nunsafe")

    def test_constructor_rejects_crlf(self):
        with self.assertRaisesRegex(ValueError, "custom header value must not contain CR/LF characters"):
            CustomHeader("X-Custom-Header", "safe\r\nX-Injected: yes")

    def test_setter_rejects_cr_lf_and_crlf(self):
        custom_header = CustomHeader("X-Custom-Header", "safe")

        for value in ("safe\runsafe", "safe\nunsafe", "safe\r\nunsafe"):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(
                    ValueError,
                    "custom header value must not contain CR/LF characters",
                ),
            ):
                custom_header.set(value)

    def test_valid_value_is_accepted_unchanged(self):
        value = "safe value; parameter=yes"
        custom_header = CustomHeader("X-Custom-Header", value)

        self.assertEqual(custom_header.header_value, value)

    def test_valid_custom_header_is_serialized_by_secure(self):
        custom_header = CustomHeader("X-Custom-Header", "custom-value")

        self.assertEqual(Secure(custom=[custom_header]).header_items(), (("X-Custom-Header", "custom-value"),))


if __name__ == "__main__":
    unittest.main()
