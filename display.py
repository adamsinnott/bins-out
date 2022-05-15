from adafruit_datetime import datetime, date, time


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def print_date(magtag, date):
  date_object = datetime.fromisoformat(date)

  day = WEEKDAYS[date_object.weekday()]
  date_number = date_object.day
  month = MONTHS[date_object.month-1]

  quadrant = 4
  scale = 2
  magtag.add_text(
    # text_font="/fonts/Arial-Bold-12.bdf",
    text_wrap=28,
    text_maxlen=120,
    text_position=(
        (magtag.graphics.display.width // quadrant),
        (magtag.graphics.display.height // 2) - 30,
    ),
    line_spacing=1,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
    text_scale=scale
  )
  magtag.add_text(
    # text_font="/fonts/Arial-Bold-12.bdf",
    text_wrap=28,
    text_maxlen=120,
    text_position=(
        (magtag.graphics.display.width // quadrant),
        (magtag.graphics.display.height // 2) - 5,
    ),
    line_spacing=0.75,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
    text_scale=scale
  )
  magtag.add_text(
    # text_font="/fonts/Arial-Bold-12.bdf",
    text_wrap=28,
    text_maxlen=120,
    text_position=(
        (magtag.graphics.display.width // quadrant),
        (magtag.graphics.display.height // 2) + 20,
    ),
    line_spacing=0.75,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
    text_scale=scale
  )
  magtag.set_text(day, index=0, auto_refresh=False)
  magtag.set_text(date_number, index=1, auto_refresh=False)
  magtag.set_text(month, index=2, auto_refresh=False)
  # magtag.refresh()

def print_icon(magtag, data):
  if data["refuse"] == True and data["garden"] == True:
    magtag.graphics.set_background("/bmps/refuse-garden.bmp")
  if data["refuse"] == True and data["garden"] == False:
    magtag.graphics.set_background("/bmps/refuse.bmp")
  if data["recycling"] == True and data["glass"] == True:
    magtag.graphics.set_background("/bmps/recycling-glass.bmp")
  if data["recycling"] == True and data["glass"] == False:
    magtag.graphics.set_background("/bmps/recycling.bmp")
  # magtag.refresh()