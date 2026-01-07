import sys
import types
import unittest
from datetime import date, datetime, time, timedelta

adafruit_datetime = types.ModuleType("adafruit_datetime")
adafruit_datetime.date = date
adafruit_datetime.datetime = datetime
adafruit_datetime.time = time
adafruit_datetime.timedelta = timedelta
sys.modules.setdefault("adafruit_datetime", adafruit_datetime)

from time_calc import difference_in_seconds, minus_hours_to_date


class TestTimeCalc(unittest.TestCase):
    def test_minus_hours_handles_offset(self):
        iso = "2025-03-30T01:30:00+01:00"
        expected = "2025-03-29T19:30:00+01:00"
        self.assertEqual(minus_hours_to_date(iso, 6), expected)

    def test_difference_in_seconds_across_offsets(self):
        base = "2025-03-30T01:00:00+00:00"
        same_instant = "2025-03-30T02:00:00+01:00"
        self.assertEqual(difference_in_seconds(base, same_instant), 0)


if __name__ == "__main__":
    unittest.main()
