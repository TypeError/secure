import unittest

from secure.headers import CrossOriginOpenerPolicy


class TestCrossOriginOpenerPolicy(unittest.TestCase):
    def test_default_coop(self):
        """Test default Cross-Origin-Opener-Policy header."""
        coop = CrossOriginOpenerPolicy()
        self.assertEqual(coop.header_value, "same-origin")

    def test_set_custom_policy(self):
        """Test setting a custom value for COOP."""
        coop = CrossOriginOpenerPolicy().set("custom-policy")
        self.assertEqual(coop.header_value, "custom-policy")

    def test_same_origin(self):
        """Test setting the COOP to 'same-origin'."""
        coop = CrossOriginOpenerPolicy().same_origin()
        self.assertEqual(coop.header_value, "same-origin")

    def test_same_origin_allow_popups(self):
        """Test setting the COOP to 'same-origin-allow-popups'."""
        coop = CrossOriginOpenerPolicy().same_origin_allow_popups()
        self.assertEqual(coop.header_value, "same-origin-allow-popups")

    def test_unsafe_none(self):
        """Test setting the COOP to 'unsafe-none'."""
        coop = CrossOriginOpenerPolicy().unsafe_none()
        self.assertEqual(coop.header_value, "unsafe-none")

    def test_clear_policy(self):
        """Test resetting the COOP to its default value."""
        coop = CrossOriginOpenerPolicy().set("custom-policy").clear()
        self.assertEqual(coop.header_value, "same-origin")


if __name__ == "__main__":
    unittest.main()
