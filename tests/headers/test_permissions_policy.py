import unittest

from secure.headers import PermissionsPolicy


class TestPermissionsPolicy(unittest.TestCase):
    def test_default_permissions_policy(self):
        """Test the default Permissions-Policy header."""
        policy = PermissionsPolicy()
        self.assertEqual(
            policy.header_value,
            "geolocation=(), microphone=(), camera=(), payment=(), fullscreen=(), usb=()",
        )

    def test_custom_permissions_policy(self):
        """Test setting custom directives in Permissions-Policy."""
        policy = PermissionsPolicy().camera("'self'").geolocation("'none'")
        self.assertEqual(policy.header_value, "camera=('self'), geolocation=('none')")

    def test_clear_permissions_policy(self):
        """Test clearing all directives in Permissions-Policy."""
        policy = PermissionsPolicy().camera("'self'").clear()
        self.assertEqual(
            policy.header_value,
            "geolocation=(), microphone=(), camera=(), payment=(), fullscreen=(), usb=()",
        )

    def test_add_directive(self):
        """Test adding a specific directive to Permissions-Policy."""
        policy = PermissionsPolicy().add_directive("microphone", "'self'")
        self.assertIn("microphone=('self')", policy.header_value)


if __name__ == "__main__":
    unittest.main()
