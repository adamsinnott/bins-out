from adafruit_datetime import datetime, date, time
import json
from time_calc import minus_hours_to_date

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
    print(f"Error: {e}")
