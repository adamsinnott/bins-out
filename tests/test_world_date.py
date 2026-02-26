import sys
import types
import unittest
from datetime import date, datetime, time, timedelta
from unittest import mock


adafruit_datetime = types.ModuleType("adafruit_datetime")
adafruit_datetime.date = date
adafruit_datetime.datetime = datetime
adafruit_datetime.time = time
adafruit_datetime.timedelta = timedelta
sys.modules.setdefault("adafruit_datetime", adafruit_datetime)

from world_date import get_current_date, TIME_URL


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


class FakeRequests:
    def __init__(self, response=None, error=None):
        self._response = response
        self._error = error
        self.last_url = None

    def get(self, url):
        self.last_url = url
        if self._error:
            raise self._error
        return self._response


class TestWorldDate(unittest.TestCase):
    def test_get_current_date_success(self):
        requests = FakeRequests(FakeResponse({"utc_time": "2026-02-26T12:34:56+00:00"}))

        result = get_current_date(requests)

        self.assertEqual(result, "2026-02-26T12:34:56+00:00")
        self.assertEqual(requests.last_url, TIME_URL)

    def test_get_current_date_returns_none_on_network_error(self):
        requests = FakeRequests(error=RuntimeError("network down"))

        with mock.patch("builtins.print"):
            result = get_current_date(requests)

        self.assertIsNone(result)

    def test_get_current_date_returns_none_on_bad_payload(self):
        requests = FakeRequests(FakeResponse({}))

        with mock.patch("builtins.print"):
            result = get_current_date(requests)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
