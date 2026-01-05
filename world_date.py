from adafruit_datetime import datetime


TIME_URL = "https://worldtimeapi.org/api/timezone/Europe/London.json"

def get_current_date(requests):
  try:
    response = requests.get(str(TIME_URL))
    json = response.json()
    date = datetime.fromisoformat(json['utc_datetime'])
    date = date.isoformat(sep='T')
    return date
  except Exception as e:
    print(f"Error getting date: {e}")