from . import darksky
from . import here
from . import utils

class WZ:

    def __init__(
            self,
            here_url,
            here_app_id,
            here_app_code,
            darksky_url,
            darksky_key
    ):

        self.here = here.Here(here_url, here_app_id, here_app_code)
        self.darksky = darksky.DarkSky(darksky_url, darksky_key)

    def _get(self, text):

        location  = self.here.location(text)

        gps_loc  = location["Location"]["NavigationPosition"][-1]
        city = location["Location"]["Address"]["City"]
        state = location["Location"]["Address"]["State"]

        weather = self.darksky.get(
            gps_loc['Latitude'],
            gps_loc['Longitude']
        )

        return(city, state, weather)

    def get(self, text, forecast=False, days=5):

        city, state, weather = self._get(text)

        current = weather["currently"]
        forecast_data = weather["daily"]["data"]

        result = None

        if forecast:
            result = f"{city}, {state} Conditions: {current['summary']} | "
            for i in range(0, days):
                result += f"\002{utils.unix_to_localtime(forecast_data[i]['time'], fmt='%a')}\002 "
                result += f"{forecast_data[i]['temperatureHigh']}({forecast_data[i]['apparentTemperatureHigh']})/{forecast_data[i]['temperatureLow']}({forecast_data[i]['apparentTemperatureLow']}) "
                result += f"{forecast_data[i]['summary']} | "
        else:

            result = (
                f"{city}, {state} Conditions: {current['summary']} | "
                f"Temp: {current['temperature']} | "
                f"High: {forecast_data[0]['temperatureHigh']}, Low: {forecast_data[0]['temperatureLow']} | "
                f"Humidity: {current['humidity']*100:.2f}% | "
                f"Sunrise: {utils.unix_to_localtime(forecast_data[0]['sunriseTime'])}, "
                f"Sunset: {utils.unix_to_localtime(forecast_data[0]['sunsetTime'])} | "
                f"Today's forecast_data: {forecast_data[0]['summary']}"
            )

        return(result)