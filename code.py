from adafruit_magtag.magtag import MagTag
from setup import connect_to_wiFi, setup_requests
from display import print_date, print_icon
import json
from adafruit_datetime import time
from utils import get_bin_collection
import alarm
import time
from time_calc import minus_hours_to_date, difference_in_seconds
from world_date import get_current_date

# Initialise variables
magtag = MagTag(default_bg=0xFFFFFF)
requests = setup_requests()
BACKGROUND_BMP="/bmps/bins-out.bmp"
CLEAR_BACKGROUND_BMP="/bmps/clear_background.bmp"
DAY_IN_SECONDS=86400
HOURS_TO_SUBTRACT=6
# setup the splash screen
# splash_screen(magtag, BACKGROUND_BMP, CLEAR_BACKGROUND_BMP)

wifi = connect_to_wiFi(magtag)
# Opening JSON file
try:
  with open('data.json', 'r') as f:
    # returns JSON object as a dictionary
    data = json.load(f)
except Exception as e:
  print(f"Error loading data.json: {e}")
  alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600)
  )

current_date = get_current_date(requests)

print('current_date')
print(current_date)

collection_data = get_bin_collection(data, current_date, HOURS_TO_SUBTRACT)

try:
  print('collection_data[date]')
  print(collection_data['date'])
  print_date(magtag, collection_data['date'])
  print_icon(magtag, collection_data)
except Exception as e:
  print(f"Error printing to the display: {e}")
magtag.refresh()

# Calculate the time.
# The date is 01-03-2025 18-00-00
# The device has just changed over
# The next pick up time is 08-03-2025 00-00-00
# The next time I need to change the date is 08-03-2025 18-00-00
# Get the current date
# Sleep time = Future date - current date
# Make the date change at a reasonable time, say 18:00 hours.

# if the change day is today
try:
  check_change_date = minus_hours_to_date(collection_data['date'], HOURS_TO_SUBTRACT)
  sleep_time = difference_in_seconds(check_change_date, current_date)
  if sleep_time <= 0:
    sleep_time = 3600
  time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)
  alarm.exit_and_deep_sleep_until_alarms(time_alarm)
except Exception as e:
  print(f"Error setting the alarm: {e}")
  alarm.exit_and_deep_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600))

# Exit the program, and then deep sleep until the alarm wakes us.
# Does not return, so we never get here.

# Check change date
# 23:59:59 - 6 == 17:59:59

# Current date
# 17:26:56 


# Check change date - current date = 
