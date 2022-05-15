import time
import ipaddress
import ssl
import wifi
import ipaddress
import ssl
import socketpool
import adafruit_requests



def connect_to_wiFi(magtag):
  # Get wifi details and more from a secrets.py file
  try:
    from secrets import secrets
  except ImportError:
    # disp("WiFi secrets are kept in secrets.py, please add them there!")
    raise

  connecting_details = "Connecting to %s" % secrets["ssid"]
  wifi.radio.connect(secrets["ssid"], secrets["password"])
  connected_details = "Connected to %s!" % secrets["ssid"]
  ip_address = "My IP address is " + str(wifi.radio.ipv4_address)

  ipv4 = ipaddress.ip_address("8.8.4.4")
  ping_details = "Ping google.com: %f ms" % (wifi.radio.ping(ipv4) * 1000)
  # magtag.set_text(connecting_details, index=0, auto_refresh=False)
  # magtag.set_text(connected_details, index=1, auto_refresh=False)
  # magtag.set_text(ip_address, index=2, auto_refresh=False)
  # magtag.set_text(ping_details, index=3, auto_refresh=False)
  # magtag.refresh()
  # time.sleep(2)
  return wifi


def setup_requests():
  pool = socketpool.SocketPool(wifi.radio)
  requests = adafruit_requests.Session(pool, ssl.create_default_context())
  return requests


def splash_screen(magtag, background, clear_background):
  magtag.graphics.set_background(background)
  magtag.refresh()
  time.sleep(5)
  magtag.graphics.set_background(clear_background)


def display_setup(magtag, lines):
  for x in range(lines):
    pos_x = 10
    y_step = 10
    if x > 1:
      pos_y = y_step * (x + 1)
    elif x == 1:
      pos_y = y_step * 2
    else:
      pos_y = y_step
    magtag.add_text(
      text_position=(pos_x, pos_y),
      text_scale=1,
    )
