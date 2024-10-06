import utime


def add_hours(date_str, hours):
    # Define your date string
    date_str = "2023-06-03T00:00:00.000000+00:00"

    # Extract the year, month, day, and time components
    date_part, time_part = date_str.split("T")
    time_part = time_part.split("+")[0]  # Removing timezone part for simplicity

    # Combine the date and time into a single string
    date_time_str = f"{date_part} {time_part[:8]}"  # Use only the hh:mm:ss part

    # Convert to a tuple
    time_tuple = utime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Convert tuple to seconds
    time_in_seconds = utime.mktime(time_tuple)

    # Add 18 hours (in seconds)
    time_in_seconds += hours * 3600

    # Convert back to a time tuple
    new_time_tuple = utime.localtime(time_in_seconds)

    # Format back to the string
    new_time_str = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000000+00:00".format(
        new_time_tuple[0], new_time_tuple[1], new_time_tuple[2], 
        new_time_tuple[3], new_time_tuple[4], new_time_tuple[5]
    )

    return new_time_str

def date_str_to_seconds(date_str):
    # Extract the date and time part, removing the timezone part
    date_part, time_part = date_str.split("T")
    time_part = time_part.split("+")[0]  # Removing timezone part

    # Combine the date and time into a single string
    date_time_str = f"{date_part} {time_part[:8]}"  # Use only the hh:mm:ss part

    # Convert to a time tuple
    time_tuple = utime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Convert to seconds since the epoch
    return utime.mktime(time_tuple)

def time_diifernce(date_str1, date_str2):
    time_in_seconds1 = date_str_to_seconds(date_str1)
    time_in_seconds2 = date_str_to_seconds(date_str2)

    time_difference = time_in_seconds1 - time_in_seconds2

    return time_difference
