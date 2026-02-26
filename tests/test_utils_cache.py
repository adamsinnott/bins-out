import sys
import types
import tempfile
import unittest
from datetime import date, datetime, time, timedelta
from unittest import mock


adafruit_datetime = types.ModuleType("adafruit_datetime")
adafruit_datetime.date = date
adafruit_datetime.datetime = datetime
adafruit_datetime.time = time
adafruit_datetime.timedelta = timedelta
sys.modules.setdefault("adafruit_datetime", adafruit_datetime)

from utils import read_cached_date, write_cached_date


class TestCachedDate(unittest.TestCase):
    def test_write_and_read_cached_date_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/last_date.txt"
            value = "2026-02-26T11:00:00+00:00"

            write_cached_date(value, path)

            self.assertEqual(read_cached_date(path), value)

    def test_falls_back_to_sleep_memory_when_filesystem_is_read_only(self):
        alarm_module = types.ModuleType("alarm")
        alarm_module.sleep_memory = bytearray(64)
        value = "2026-02-26T12:00:00+00:00"

        with mock.patch.dict(sys.modules, {"alarm": alarm_module}, clear=False):
            with mock.patch("builtins.print"):
                with mock.patch("builtins.open", side_effect=OSError(30, "Read-only file system")):
                    write_cached_date(value, "last_date.txt")

                with mock.patch("builtins.open", side_effect=OSError(2, "No such file")):
                    result = read_cached_date("last_date.txt")

        self.assertEqual(result, value)

    def test_sleep_memory_is_not_written_if_value_too_long(self):
        alarm_module = types.ModuleType("alarm")
        alarm_module.sleep_memory = bytearray(4)
        value = "2026-02-26T12:00:00+00:00"

        with mock.patch.dict(sys.modules, {"alarm": alarm_module}, clear=False):
            with mock.patch("builtins.print"):
                with mock.patch("builtins.open", side_effect=OSError(30, "Read-only file system")):
                    write_cached_date(value, "last_date.txt")
                with mock.patch("builtins.open", side_effect=OSError(2, "No such file")):
                    result = read_cached_date("last_date.txt")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
