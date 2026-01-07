from adafruit_datetime import datetime
import json
from time_calc import minus_hours_to_date

def show_message(magtag, clear_background_bmp, message):
  magtag.graphics.set_background(clear_background_bmp)
  magtag.add_text(
    text_wrap=28,
    text_maxlen=120,
    text_position=(
      magtag.graphics.display.width // 2,
      magtag.graphics.display.height // 2,
    ),
    line_spacing=0.9,
    text_anchor_point=(0.5, 0.5),
    text_scale=2
  )
  magtag.set_text(message, index=0, auto_refresh=False)
  magtag.refresh()

def _get_alarm_module():
  try:
    import alarm
    return alarm
  except Exception:
    return None

def write_cached_date(date_value, last_date_path):
  if not date_value:
    return
  try:
    with open(last_date_path, 'w') as f:
      f.write(date_value)
    return
  except OSError as e:
    if getattr(e, "errno", None) == 30:
      print("Filesystem is read-only; caching in sleep memory.")
    else:
      print(f"Error caching last_date to file: {e}")
  alarm_module = _get_alarm_module()
  if not alarm_module or not hasattr(alarm_module, "sleep_memory"):
    return
  try:
    data = date_value.encode("utf-8")
    max_len = len(alarm_module.sleep_memory) - 1
    if len(data) > max_len:
      print("Cached date too long for sleep memory.")
      return
    alarm_module.sleep_memory[0] = len(data)
    alarm_module.sleep_memory[1:1 + len(data)] = data
  except Exception as e:
    print(f"Error caching last_date in sleep memory: {e}")

def read_cached_date(last_date_path):
  try:
    with open(last_date_path, 'r') as f:
      cached_date = f.read().strip()
    if cached_date:
      return cached_date
  except OSError as e:
    if getattr(e, "errno", None) != 2:
      print(f"Error reading cached date file: {e}")
  alarm_module = _get_alarm_module()
  if not alarm_module or not hasattr(alarm_module, "sleep_memory"):
    return None
  try:
    if len(alarm_module.sleep_memory) < 2:
      return None
    length = alarm_module.sleep_memory[0]
    if length <= 0 or length > (len(alarm_module.sleep_memory) - 1):
      return None
    data = bytes(alarm_module.sleep_memory[1:1 + length])
    cached_date = data.decode("utf-8").strip()
    return cached_date or None
  except Exception as e:
    print(f"Error reading cached date from sleep memory: {e}")
  return None

def get_bin_collection(data, current_date, HOURS_TO_SUBTRACT):
  try:
    current_collection = json.loads('{"date": "2021-01-01T00:00:00.000000+00:00","garden": false,"refuse": false,"glass": false,"recycling": false,"bhChange": false}')
    current_timestamp = datetime.fromisoformat(current_date).timestamp()
    placeholder_timestamp = 4808275075
    for collection in data['dates']:
      # collection_date = datetime.fromisoformat(collection['date'])
      collection_date = datetime.fromisoformat(minus_hours_to_date(collection['date'], HOURS_TO_SUBTRACT))
      collection_timestamp = collection_date.timestamp()
      if current_timestamp < collection_timestamp:
        if (collection_timestamp < placeholder_timestamp or not placeholder_timestamp):
          placeholder_timestamp = collection_timestamp
          current_collection = collection
    return current_collection

  except Exception as e:
    print(f"Error getting bin collection data: {e}")
