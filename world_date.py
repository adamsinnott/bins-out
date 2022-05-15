from adafruit_datetime import datetime, date, time


TIME_URL = "https://worldtimeapi.org/api/timezone/Europe/London.json"

def get_date(requests):
  response = requests.get(str(TIME_URL))
  json = response.json()
  date = datetime.fromisoformat(json['datetime'])
  return date.timestamp()
