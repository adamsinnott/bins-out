from adafruit_datetime import datetime

TIME_URL = "https://timeapi.io/api/v1/timezone/zone?timeZone=Europe%2FLondon"

def get_current_date(requests):
  try:
    response = requests.get(str(TIME_URL))
    json = response.json()
    date = datetime.fromisoformat(json['utc_time'])
    date = date.isoformat(sep='T')
    return date
  except Exception as e:
    print(f"Error getting date: {e}")