import os
import runpy
import sys
import types
import io
import unittest
from unittest import mock


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CODE_PATH = os.path.join(PROJECT_ROOT, "code.py")


class SleepExit(BaseException):
    pass


class FakeGraphics:
    def __init__(self):
        self.display = types.SimpleNamespace(width=296, height=128)
        self.background = None

    def set_background(self, background):
        self.background = background


class FakeMagTag:
    instances = []

    def __init__(self, default_bg=None):
        self.default_bg = default_bg
        self.graphics = FakeGraphics()
        self.text_by_index = {}
        self.add_text_calls = []
        self.refresh_calls = 0
        FakeMagTag.instances.append(self)

    def add_text(self, **kwargs):
        self.add_text_calls.append(kwargs)

    def set_text(self, text, index=0, auto_refresh=False):
        self.text_by_index[index] = text

    def refresh(self):
        self.refresh_calls += 1


class TestCodeRuntime(unittest.TestCase):
    def _run_code_with_stubs(
        self,
        current_date,
        cached_date,
        sleep_seconds,
        collection_date="2026-03-01T12:00:00+00:00",
    ):
        FakeMagTag.instances = []
        calls = {
            "show_message": [],
            "print_date": [],
            "print_icon": [],
            "write_cached_date": [],
            "read_cached_date": [],
            "sleep_monotonic": [],
        }

        adafruit_magtag_pkg = types.ModuleType("adafruit_magtag")
        adafruit_magtag_mod = types.ModuleType("adafruit_magtag.magtag")
        adafruit_magtag_mod.MagTag = FakeMagTag
        adafruit_magtag_pkg.magtag = adafruit_magtag_mod

        setup_mod = types.ModuleType("setup")
        setup_mod.connect_to_wiFi = lambda magtag: "wifi"
        setup_mod.setup_requests = lambda: "requests"

        display_mod = types.ModuleType("display")

        def print_date(magtag, date_value):
            calls["print_date"].append(date_value)

        def print_icon(magtag, data):
            calls["print_icon"].append(data)

        display_mod.print_date = print_date
        display_mod.print_icon = print_icon

        utils_mod = types.ModuleType("utils")

        def get_bin_collection(data, now, hours):
            return {
                "date": collection_date,
                "garden": False,
                "refuse": True,
                "glass": False,
                "recycling": False,
                "bhChange": False,
            }

        def show_message(magtag, background, message):
            calls["show_message"].append(message)

        def write_cached_date(value, path):
            calls["write_cached_date"].append((value, path))

        def read_cached_date(path):
            calls["read_cached_date"].append(path)
            return cached_date

        utils_mod.get_bin_collection = get_bin_collection
        utils_mod.show_message = show_message
        utils_mod.write_cached_date = write_cached_date
        utils_mod.read_cached_date = read_cached_date

        time_calc_mod = types.ModuleType("time_calc")
        time_calc_mod.minus_hours_to_date = lambda value, hrs: "2026-03-01T18:00:00+00:00"
        time_calc_mod.difference_in_seconds = lambda a, b: sleep_seconds

        world_date_mod = types.ModuleType("world_date")
        world_date_mod.get_current_date = lambda requests: current_date

        alarm_mod = types.ModuleType("alarm")

        class TimeAlarm:
            def __init__(self, monotonic_time):
                self.monotonic_time = monotonic_time

        def exit_and_deep_sleep_until_alarms(time_alarm):
            calls["sleep_monotonic"].append(time_alarm.monotonic_time)
            raise SleepExit()

        alarm_mod.time = types.SimpleNamespace(TimeAlarm=TimeAlarm)
        alarm_mod.exit_and_deep_sleep_until_alarms = exit_and_deep_sleep_until_alarms

        fake_time_mod = types.ModuleType("time")
        fake_time_mod.monotonic = lambda: 100

        real_open = open

        def fake_open(path, mode="r", *args, **kwargs):
            if str(path) == "data.json" and "r" in mode:
                return io.StringIO(
                    (
                        '{"dates":[{"date":"2026-03-01T12:00:00+00:00",'
                        '"garden":false,"refuse":true,"glass":false,'
                        '"recycling":false,"bhChange":false}]}'
                    )
                )
            return real_open(path, mode, *args, **kwargs)

        with mock.patch.dict(
            sys.modules,
            {
                "adafruit_magtag": adafruit_magtag_pkg,
                "adafruit_magtag.magtag": adafruit_magtag_mod,
                "setup": setup_mod,
                "display": display_mod,
                "utils": utils_mod,
                "time_calc": time_calc_mod,
                "world_date": world_date_mod,
                "alarm": alarm_mod,
                "time": fake_time_mod,
            },
            clear=False,
        ):
            with mock.patch("builtins.open", side_effect=fake_open):
                with mock.patch("builtins.print"):
                    with self.assertRaises(SleepExit):
                        runpy.run_path(CODE_PATH, run_name="__main__")

        return calls, FakeMagTag.instances[-1]

    def test_offline_branch_shows_offline_and_sleeps_default(self):
        calls, _ = self._run_code_with_stubs(current_date=None, cached_date=None, sleep_seconds=7200)

        self.assertEqual(calls["show_message"], ["OFFLINE"])
        self.assertEqual(calls["sleep_monotonic"], [3700])

    def test_stale_branch_caps_sleep_and_marks_display(self):
        calls, magtag = self._run_code_with_stubs(
            current_date=None,
            cached_date="2026-02-26T12:00:00+00:00",
            sleep_seconds=7200,
        )

        self.assertEqual(calls["show_message"], [])
        self.assertEqual(calls["sleep_monotonic"], [3700])
        self.assertEqual(calls["print_date"], ["2026-03-01T12:00:00+00:00"])
        self.assertEqual(magtag.text_by_index.get(3), "STALE")

    def test_no_more_dates_branch_shows_message_and_sleeps_one_day(self):
        calls, _ = self._run_code_with_stubs(
            current_date="2026-02-26T12:00:00+00:00",
            cached_date=None,
            sleep_seconds=0,
        )

        self.assertEqual(calls["show_message"], ["NO MORE DATES"])
        self.assertEqual(calls["sleep_monotonic"], [86500])


if __name__ == "__main__":
    unittest.main()
