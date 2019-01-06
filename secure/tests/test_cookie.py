import datetime
import unittest

from freezegun import freeze_time

from secure.cookie import cookie_expiration

@freeze_time('2019-01-06 20:26:09')
class TestCookie(unittest.TestCase):
    def test_cookie_expiration(self):
        hours = 2 
        self.assertEqual(cookie_expiration(hours), 'Sun, 06 Jan 2019 22:26:09 GMT')
        self.assertEqual(cookie_expiration(hours, timedelta_obj=True), datetime.timedelta(hours=hours))
