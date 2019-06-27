import re

us = re.compile("^\\d{5}(-{0,1}\\d{4})?$")
ca = re.compile("([ABCEGHJKLMNPRSTVXY]\d)([ABCEGHJKLMNPRSTVWXYZ]\d){2}", re.IGNORECASE)

def unix_to_localtime(t, tz="US/Eastern", fmt="%H:%M:%S"):
    """
    Convert unix timestamp to local time.
    """

    from datetime import datetime
    from pytz import timezone
    import pytz

    utc = pytz.utc
    tz = timezone(tz)

    timestamp = datetime.utcfromtimestamp(t)

    return(utc.localize(timestamp).astimezone(tz).strftime(fmt))

def postal_code(string):
    """
    Check for United States and Canadian postal codes
    """

    if us.match(string):
        return "USA";
    elif ca.match(string):
        return "CAN";
    else:
        return None
