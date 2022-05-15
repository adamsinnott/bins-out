from adafruit_magtag.magtag import MagTag
from setup import splash_screen, connect_to_wiFi, setup_requests
from display import print_date, print_icon
import json
from adafruit_datetime import time
from utils import get_bin_collection
import alarm
import time

# Initialise variables
magtag = MagTag(default_bg=0xFFFFFF)
requests = setup_requests()
BACKGROUND_BMP="/bmps/bins-out.bmp"
CLEAR_BACKGROUND_BMP="/bmps/clear_background.bmp"
DAY_IN_SECONDS=86400
# setup the splash screen
# splash_screen(magtag, BACKGROUND_BMP, CLEAR_BACKGROUND_BMP)

wifi = connect_to_wiFi(magtag)

# Opening JSON file
f = open('data.json')
# returns JSON object as
# a dictionary
data = json.load(f)

collection_data = get_bin_collection(data, requests)

print_date(magtag, collection_data['date'])
print_icon(magtag, collection_data)
magtag.refresh()
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DAY_IN_SECONDS)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
