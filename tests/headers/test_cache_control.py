import unittest

from secure.headers import CacheControl


class TestCacheControl(unittest.TestCase):
    def test_default_cache_control(self):
        """Test default Cache-Control value (no-store, no-cache, must-revalidate)."""
        cache_control = CacheControl()
        self.assertEqual(
            cache_control.header_value, "no-store, no-cache, must-revalidate"
        )

    def test_set_no_cache(self):
        """Test adding the no-cache directive to Cache-Control."""
        cache_control = CacheControl().no_cache()
        self.assertIn("no-cache", cache_control.header_value)

    def test_set_max_age(self):
        """Test setting a max-age directive in Cache-Control."""
        cache_control = CacheControl().max_age(3600)
        self.assertIn("max-age=3600", cache_control.header_value)

    def test_clear_cache_control(self):
        """Test clearing Cache-Control directives."""
        cache_control = CacheControl().no_cache().clear()
        self.assertEqual(
            cache_control.header_value, "no-store, no-cache, must-revalidate"
        )

    def test_multiple_directives(self):
        """Test adding multiple Cache-Control directives."""
        cache_control = CacheControl().no_cache().must_revalidate().max_age(3600)
        self.assertEqual(
            cache_control.header_value, "no-cache, must-revalidate, max-age=3600"
        )


if __name__ == "__main__":
    unittest.main()
