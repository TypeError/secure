import unittest

from secure.headers import XFrameOptions


class TestXFrameOptions(unittest.TestCase):
    def test_default_x_frame_options(self):
        """Test default X-Frame-Options value (SAMEORIGIN)."""
        xfo = XFrameOptions()
        self.assertEqual(xfo.header_value, "SAMEORIGIN")

    def test_set_deny(self):
        """Test setting X-Frame-Options to DENY."""
        xfo = XFrameOptions().deny()
        self.assertEqual(xfo.header_value, "DENY")

    def test_set_sameorigin(self):
        """Test explicitly setting X-Frame-Options to SAMEORIGIN."""
        xfo = XFrameOptions().sameorigin()
        self.assertEqual(xfo.header_value, "SAMEORIGIN")


if __name__ == "__main__":
    unittest.main()
