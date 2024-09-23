import unittest

from secure.headers import ContentSecurityPolicy


class TestContentSecurityPolicy(unittest.TestCase):
    def test_default_csp(self):
        """Test default Content-Security-Policy header."""
        csp = ContentSecurityPolicy()
        self.assertEqual(
            csp.header_value,
            "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
        )

    def test_custom_policy(self):
        """Test setting custom directives for CSP."""
        csp = (
            ContentSecurityPolicy()
            .default_src("'self'")
            .img_src("'self'", "cdn.example.com")
        )
        self.assertEqual(
            csp.header_value, "default-src 'self'; img-src 'self' cdn.example.com"
        )

    def test_add_script_src(self):
        """Test adding script-src directive."""
        csp = ContentSecurityPolicy().script_src("'self'", "'unsafe-inline'")
        self.assertIn("script-src 'self' 'unsafe-inline'", csp.header_value)

    def test_clear_policy(self):
        """Test clearing CSP directives."""
        csp = ContentSecurityPolicy().default_src("'self'").clear()
        self.assertEqual(
            csp.header_value,
            "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
        )


if __name__ == "__main__":
    unittest.main()
