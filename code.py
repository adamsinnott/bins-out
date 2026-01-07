from adafruit_magtag.magtag import MagTag
from setup import connect_to_wiFi, setup_requests
from display import print_date, print_icon
import json
from utils import get_bin_collection, show_message, write_cached_date, read_cached_date
import alarm
import time
from time_calc import minus_hours_to_date, difference_in_seconds
from world_date import get_current_date

# Initialise variables
magtag = MagTag(default_bg=0xFFFFFF)
# setup request runs before wifi connection otherwise it fails
requests = setup_requests()
BACKGROUND_BMP="/bmps/bins-out.bmp"
CLEAR_BACKGROUND_BMP="/bmps/clear_background.bmp"
DAY_IN_SECONDS=86400
HOURS_TO_SUBTRACT=6
LAST_DATE_PATH="last_date.txt"
DEFAULT_SLEEP_SECONDS=3600

wifi = connect_to_wiFi(magtag)
# Opening JSON file
try:
  with open('data.json', 'r') as f:
    # returns JSON object as a dictionary
    data = json.load(f)
except Exception as e:
  print(f"Error loading data.json: {e}")
  alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DEFAULT_SLEEP_SECONDS)
  )

current_date = get_current_date(requests)
stale_date = False
if current_date:
  write_cached_date(current_date, LAST_DATE_PATH)
else:
  cached_date = read_cached_date(LAST_DATE_PATH)
  if cached_date:
    current_date = cached_date
    stale_date = True

if not current_date:
  print("No current date available; sleeping.")
  show_message(magtag, CLEAR_BACKGROUND_BMP, "OFFLINE")
  alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DEFAULT_SLEEP_SECONDS)
  )
print('current_date')
print(current_date)

collection_data = get_bin_collection(data, current_date, HOURS_TO_SUBTRACT)
try:
  check_change_date = minus_hours_to_date(collection_data['date'], HOURS_TO_SUBTRACT)
  sleep_time = difference_in_seconds(check_change_date, current_date)
  if stale_date and sleep_time > 0:
    sleep_time = min(sleep_time, DEFAULT_SLEEP_SECONDS)
except Exception as e:
  print(f"Error calculating sleep time: {e}")
  alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DEFAULT_SLEEP_SECONDS)
  )

if sleep_time <= 0:
  show_message(magtag, CLEAR_BACKGROUND_BMP, "NO MORE DATES")
  alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DAY_IN_SECONDS)
  )

try:
  print('collection_data[date]')
  print(collection_data['date'])
  print_date(magtag, collection_data['date'])
  print_icon(magtag, collection_data)
  if stale_date:
    magtag.add_text(
      text_position=(magtag.graphics.display.width - 5, 5),
      text_anchor_point=(1.0, 0.0),
      text_scale=1
    )
    magtag.set_text("STALE", index=3, auto_refresh=False)
except Exception as e:
  print(f"Error printing to the display: {e}")
magtag.refresh()

try:
  time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)
  alarm.exit_and_deep_sleep_until_alarms(time_alarm)
except Exception as e:
  print(f"Error setting the alarm: {e}")
  alarm.exit_and_deep_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DEFAULT_SLEEP_SECONDS))

# Exit the program, and then deep sleep until the alarm wakes us.
# Does not return, so we never get here.
