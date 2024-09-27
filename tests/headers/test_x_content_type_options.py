import unittest

from secure.headers import XContentTypeOptions


class TestXContentTypeOptions(unittest.TestCase):
    def test_default_x_content_type_options(self):
        """Test default X-Content-Type-Options header."""
        x_content_type_options = XContentTypeOptions()
        self.assertEqual(x_content_type_options.header_value, "nosniff")

    def test_set_custom_value(self):
        """Test setting a custom value for X-Content-Type-Options."""
        x_content_type_options = XContentTypeOptions().set("custom-value")
        self.assertEqual(x_content_type_options.header_value, "custom-value")

    def test_nosniff(self):
        """Test setting the X-Content-Type-Options to 'nosniff'."""
        x_content_type_options = XContentTypeOptions().nosniff()
        self.assertEqual(x_content_type_options.header_value, "nosniff")

    def test_clear(self):
        """Test clearing and resetting the X-Content-Type-Options to default."""
        x_content_type_options = XContentTypeOptions().set("custom-value").clear()
        self.assertEqual(x_content_type_options.header_value, "nosniff")


if __name__ == "__main__":
    unittest.main()
