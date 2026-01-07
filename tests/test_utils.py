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

from utils import get_bin_collection


class TestGetBinCollection(unittest.TestCase):
    def test_selects_next_future_collection(self):
        data = {
            "dates": [
                {"date": "2025-01-02T00:00:00+00:00", "garden": False, "refuse": True, "glass": False, "recycling": False, "bhChange": False},
                {"date": "2025-01-09T00:00:00+00:00", "garden": False, "refuse": False, "glass": True, "recycling": True, "bhChange": False},
            ]
        }
        current_date = "2025-01-01T12:00:00+00:00"

        result = get_bin_collection(data, current_date, 6)

        self.assertEqual(result["date"], "2025-01-02T00:00:00+00:00")

    def test_returns_placeholder_when_no_future_dates(self):
        data = {
            "dates": [
                {"date": "2025-01-02T00:00:00+00:00", "garden": False, "refuse": True, "glass": False, "recycling": False, "bhChange": False},
            ]
        }
        current_date = "2025-02-01T00:00:00+00:00"

        result = get_bin_collection(data, current_date, 6)

        self.assertEqual(result["date"], "2021-01-01T00:00:00.000000+00:00")


if __name__ == "__main__":
    unittest.main()
