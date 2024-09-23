import unittest

from secure.headers import StrictTransportSecurity


class TestStrictTransportSecurity(unittest.TestCase):
    def test_default_hsts(self):
        """Test default Strict-Transport-Security header."""
        hsts = StrictTransportSecurity()
        self.assertEqual(hsts.header_name, "Strict-Transport-Security")
        self.assertEqual(hsts.header_value, "max-age=31536000")

    def test_custom_max_age(self):
        """Test setting a custom max-age for HSTS."""
        hsts = StrictTransportSecurity().max_age(31536000)
        self.assertEqual(hsts.header_value, "max-age=31536000")

    def test_preload(self):
        """Test adding preload directive to HSTS."""
        hsts = StrictTransportSecurity().preload()
        self.assertIn("preload", hsts.header_value)

    def test_include_subdomains(self):
        """Test adding includeSubDomains directive to HSTS."""
        hsts = StrictTransportSecurity().max_age(31536000).include_subdomains()
        self.assertIn("includeSubDomains", hsts.header_value)


if __name__ == "__main__":
    unittest.main()
