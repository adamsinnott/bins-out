from adafruit_magtag.magtag import MagTag
from setup import splash_screen, connect_to_wiFi, setup_requests
from display import print_date, print_icon
import json
from adafruit_datetime import time
from utils import get_bin_collection
import alarm
import time
from world_date import get_date
from time_calc import add_hours, time_diifernce


# Initialise variables
magtag = MagTag(default_bg=0xFFFFFF)
requests = setup_requests()
BACKGROUND_BMP="/bmps/bins-out.bmp"
CLEAR_BACKGROUND_BMP="/bmps/clear_background.bmp"
# DAY_IN_SECONDS=86400
# setup the splash screen
# splash_screen(magtag, BACKGROUND_BMP, CLEAR_BACKGROUND_BMP)

wifi = connect_to_wiFi(magtag)

# Opening JSON file
f = open('data.json')
# returns JSON object as
# a dictionary
data = json.load(f)

current_timestamp = get_date(requests)

collection_data = get_bin_collection(data, requests, current_timestamp)

print_date(magtag, collection_data['date'])
print_icon(magtag, collection_data)
magtag.refresh()

# Calculate the time.
# The date is 01-03-2025 18-00-00
# The device has just changed over
# The next pick up time is 08-03-2025 00-00-00
# The next time I need to change the date is 08-03-2025 18-00-00
# Get the current date
# Sleep time = Future date - current date
change_date = add_hours(collection_data['date'], 18)
sleep_time = time_diifernce(change_date, current_timestamp) 

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
