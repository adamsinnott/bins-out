import adafruit_datetime

def minus_hours_to_date(iso_date, hours_to_add):
    # Parse the ISO 8601 date string into a datetime object
    dt = adafruit_datetime.datetime.fromisoformat(iso_date)
    # Create a timedelta object for the number of hours to add
    delta = adafruit_datetime.timedelta(hours=hours_to_add)
    
    # Add the timedelta to the datetime object
    new_dt = dt - delta
    
    # Return the new datetime as an ISO 8601 formatted string
    return new_dt.isoformat()

def difference_in_seconds(iso_date1, iso_date2):
    # Parse the ISO 8601 date strings into datetime objects
    dt1 = adafruit_datetime.datetime.fromisoformat(iso_date1)
    dt2 = adafruit_datetime.datetime.fromisoformat(iso_date2)
    
    # Find the difference between the two datetime objects
    delta = dt1 - dt2
    
    # Get the total difference in seconds
    return delta.total_seconds()