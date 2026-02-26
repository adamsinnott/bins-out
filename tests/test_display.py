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

from display import print_date, print_icon


class FakeGraphics:
    def __init__(self):
        self.display = types.SimpleNamespace(width=296, height=128)
        self.background = None

    def set_background(self, background):
        self.background = background


class FakeMagTag:
    def __init__(self):
        self.graphics = FakeGraphics()
        self.text_by_index = {}
        self.text_calls = []

    def add_text(self, **kwargs):
        self.text_calls.append(kwargs)

    def set_text(self, value, index=0, auto_refresh=False):
        self.text_by_index[index] = value


class TestDisplay(unittest.TestCase):
    def test_print_date_renders_day_date_month(self):
        magtag = FakeMagTag()

        print_date(magtag, "2026-02-26T12:00:00+00:00")

        self.assertEqual(magtag.text_by_index[0], "Thursday")
        self.assertEqual(magtag.text_by_index[1], 26)
        self.assertEqual(magtag.text_by_index[2], "February")

    def test_print_icon_refuse_garden(self):
        magtag = FakeMagTag()

        print_icon(magtag, {"refuse": True, "garden": True, "recycling": False, "glass": False})

        self.assertEqual(magtag.graphics.background, "/bmps/refuse-garden.bmp")

    def test_print_icon_refuse_only(self):
        magtag = FakeMagTag()

        print_icon(magtag, {"refuse": True, "garden": False, "recycling": False, "glass": False})

        self.assertEqual(magtag.graphics.background, "/bmps/refuse.bmp")

    def test_print_icon_recycling_glass(self):
        magtag = FakeMagTag()

        print_icon(magtag, {"refuse": False, "garden": False, "recycling": True, "glass": True})

        self.assertEqual(magtag.graphics.background, "/bmps/recycling-glass.bmp")

    def test_print_icon_recycling_only(self):
        magtag = FakeMagTag()

        print_icon(magtag, {"refuse": False, "garden": False, "recycling": True, "glass": False})

        self.assertEqual(magtag.graphics.background, "/bmps/recycling.bmp")


if __name__ == "__main__":
    unittest.main()
