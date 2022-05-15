from adafruit_datetime import datetime, date, time
from world_date import get_date
import json


def get_bin_collection(data, requests):
  current_timestamp = get_date(requests)
  current_collection = json.loads('{"date": "2021-01-01T00:00:00.000000+00:00","garden": false,"refuse": false,"glass": false,"recycling": false,"bhChange": false}')
  placeholder_timestamp = 4808275075
  for collection in data['dates']:
    collection_date = datetime.fromisoformat(collection['date'])
    collection_timestamp = collection_date.timestamp()
    if current_timestamp < collection_timestamp:
      if (collection_timestamp < placeholder_timestamp or not placeholder_timestamp):
        placeholder_timestamp = collection_timestamp
        current_collection = collection
  return current_collection
