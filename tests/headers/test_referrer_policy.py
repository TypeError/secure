import unittest

from secure.headers import ReferrerPolicy


class TestReferrerPolicy(unittest.TestCase):
    def test_default_referrer_policy(self):
        """Test default Referrer-Policy header."""
        referrer_policy = ReferrerPolicy()
        self.assertEqual(
            referrer_policy.header_value, "strict-origin-when-cross-origin"
        )

    def test_set_custom_policy(self):
        """Test setting a custom referrer policy."""
        referrer_policy = ReferrerPolicy().set("no-referrer")
        self.assertEqual(referrer_policy.header_value, "no-referrer")

    def test_no_referrer(self):
        """Test setting the Referrer-Policy to 'no-referrer'."""
        referrer_policy = ReferrerPolicy().no_referrer()
        self.assertEqual(referrer_policy.header_value, "no-referrer")

    def test_no_referrer_when_downgrade(self):
        """Test setting the Referrer-Policy to 'no-referrer-when-downgrade'."""
        referrer_policy = ReferrerPolicy().no_referrer_when_downgrade()
        self.assertEqual(referrer_policy.header_value, "no-referrer-when-downgrade")

    def test_origin(self):
        """Test setting the Referrer-Policy to 'origin'."""
        referrer_policy = ReferrerPolicy().origin()
        self.assertEqual(referrer_policy.header_value, "origin")

    def test_origin_when_cross_origin(self):
        """Test setting the Referrer-Policy to 'origin-when-cross-origin'."""
        referrer_policy = ReferrerPolicy().origin_when_cross_origin()
        self.assertEqual(referrer_policy.header_value, "origin-when-cross-origin")

    def test_same_origin(self):
        """Test setting the Referrer-Policy to 'same-origin'."""
        referrer_policy = ReferrerPolicy().same_origin()
        self.assertEqual(referrer_policy.header_value, "same-origin")

    def test_strict_origin(self):
        """Test setting the Referrer-Policy to 'strict-origin'."""
        referrer_policy = ReferrerPolicy().strict_origin()
        self.assertEqual(referrer_policy.header_value, "strict-origin")

    def test_strict_origin_when_cross_origin(self):
        """Test setting the Referrer-Policy to 'strict-origin-when-cross-origin'."""
        referrer_policy = ReferrerPolicy().strict_origin_when_cross_origin()
        self.assertEqual(
            referrer_policy.header_value, "strict-origin-when-cross-origin"
        )

    def test_unsafe_url(self):
        """Test setting the Referrer-Policy to 'unsafe-url'."""
        referrer_policy = ReferrerPolicy().unsafe_url()
        self.assertEqual(referrer_policy.header_value, "unsafe-url")

    def test_clear_policy(self):
        """Test clearing the referrer policy directives and resetting to default."""
        referrer_policy = ReferrerPolicy().set("custom-policy").clear()
        self.assertEqual(
            referrer_policy.header_value, "strict-origin-when-cross-origin"
        )


if __name__ == "__main__":
    unittest.main()
