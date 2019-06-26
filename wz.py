import sopel.module

here_url = "https://geocoder.api.here.com/6.2/geocode.json"
here_app_id = ""
here_app_code = ""

darksky_url = "https://api.darksky.net/forecast"
darksky_key = ""


def unix_to_localtime(t, tz="US/Eastern"):
    """
    Convert unix timestamp to local time.
    """

    from datetime import datetime
    from pytz import timezone
    import pytz

    utc = pytz.utc
    tz = timezone(tz)

    timestamp = datetime.utcfromtimestamp(t)

    return(utc.localize(timestamp).astimezone(tz).strftime("%H:%M:%S"))


def get_temp_by_zip(zipcode):
    """
    """

    import requests

    location = requests.get(
        here_url,
        params={
            "app_id": here_app_id,
            "app_code": here_app_code,
            "postalcode": zipcode
        }
    )

    location_match = None
    for result in location.json()["Response"]["View"][-1]["Result"]:
        if result["Location"]["Address"]["Country"] in ["USA", "CAN"]:
            location_match = result
            break

    else:
        return(f"Unable to find a proper match for {zipcode}")

    city = location_match["Location"]["Address"]["City"]
    state = location_match["Location"]["Address"]["State"]

    gps_loc = location_match["Location"]["NavigationPosition"][-1]

    darksky_data = requests.get(
        f"{darksky_url}/{darksky_key}/{gps_loc['Latitude']},{gps_loc['Longitude']}"
    )

    current = darksky_data.json()["currently"]
    forecast = darksky_data.json()["daily"]["data"]

    return(
        f"{city}, {state} Conditions: {current['summary']} | "
        f"Temp: {current['temperature']} | "
        f"High: {forecast[0]['temperatureHigh']}, Low: {forecast[0]['temperatureLow']} | "
        f"Humidity: {current['humidity']*100:.2f}% | "
        f"Sunrise: {unix_to_localtime(forecast[0]['sunriseTime'])}, "
        f"Sunset: {unix_to_localtime(forecast[0]['sunsetTime'])} | "
        f"Today's Forecast: {forecast[0]['summary']}"
    )


@sopel.module.commands('wz')
def weatherbot(bot, trigger):
    bot.say(get_temp_by_zip(trigger.group(2)))


if __name__ == "__main__":
    print(get_temp_by_zip('K4R1E5'))
