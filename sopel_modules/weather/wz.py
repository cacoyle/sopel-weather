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

    def __uv_rating(self, index):
        if 1 <= index <= 2:
            # Green
            return(f"\x0303{index}\x03")
        if 3 <= index <= 5:
            # Yellow
            return(f"\x0308{index}\x03")
        if 6 <= index <= 7:
            # Orange
            return(f"\x0307{index}\x03")
        if 8 <= index <= 10:
            # Red
            return(f"\x0304{index}\x03")
        if index > 10:
            # Purple
            return(f"\x0306{index}\x03")

    def _get(self, text):

        location = self.here.location(text)

        gps_loc = location["Location"]["NavigationPosition"][-1]
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
            def f(i):
                r = f"\002{utils.unix_to_localtime(forecast_data[i]['time'], fmt='%a')}\002 "
                r += f"{forecast_data[i]['temperatureHigh']}({forecast_data[i]['apparentTemperatureHigh']})/{forecast_data[i]['temperatureLow']}({forecast_data[i]['apparentTemperatureLow']}) "
                r += f"{forecast_data[i]['summary']}"
                return r
            result += ' | '.join([f(x) for x in range(0, days)])
        else:

            result = (
                f"{city}, {state} Conditions: {current['summary']} | "
                f"Temp: {current['temperature']}, Feels-Like: {current['apparentTemperature']} | "
                f"UV Index: {self.__uv_rating(current['uvIndex'])} |"
                f"High: {forecast_data[0]['temperatureHigh']}, Low: {forecast_data[0]['temperatureLow']} | "
                f"Humidity: {current['humidity']*100:.2f}% | "
                f"Sunrise: {utils.unix_to_localtime(forecast_data[0]['sunriseTime'])}, "
                f"Sunset: {utils.unix_to_localtime(forecast_data[0]['sunsetTime'])} | "
                f"Today's Forecast: {forecast_data[0]['summary']}"
            )

        return(result)
