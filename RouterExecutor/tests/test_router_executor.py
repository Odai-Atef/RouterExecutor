import json
from datetime import timedelta, datetime, timezone
from unittest import TestCase
from freezegun import freeze_time

from RouterExecutor.RouterExecutor import RouterExecutor


class JWTTest(TestCase):

    def setUp(self):
        self.router_executor = RouterExecutor('test')
        self.message = {
            'iss': 'joe',
            'exp': 1300819380,
            'http://example.com/is_root': True,
        }


    @freeze_time("2011-03-22 18:00:00", tz_offset=0)
    def test_consumer(self):
        self.router_executor.consume()
        # self.assertEqual(message, self.message)

