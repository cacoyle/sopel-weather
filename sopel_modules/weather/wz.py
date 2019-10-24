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

    def get(self, text, kind="current", **kwargs):

        city, state, weather = self._get(text)

        current = weather["currently"]
        forecast_data = weather["daily"]["data"]
        hourly = weather['hourly']['data']
        tz = weather['timezone']

        result = None

        if kind == "forecast":
            result = f"{city}, {state} Conditions: {current['summary']} | {weather['daily']['summary']} | "
            def f(i):
                fd = forecast_data[i]
                day = utils.unix_to_localtime(fd['time'], tz=tz, fmt='%a')
                return (
                   f"\002{day}\002 "
                   f"{fd['temperatureHigh']}({fd['apparentTemperatureHigh']})/{fd['temperatureLow']}({fd['apparentTemperatureLow']}) "
                   f"{fd['summary']}"
                )
                return r
            result += ' | '.join([f(x) for x in range(0, kwargs['days'])])
        elif kind == "current":
            sunrise = utils.unix_to_localtime(forecast_data[0]['sunriseTime'], tz=tz)
            sunset = utils.unix_to_localtime(forecast_data[0]['sunsetTime'], tz=tz)
            result = (
                f"{city}, {state} Conditions: {current['summary']} | "
                f"Temp: {current['temperature']}, Feels-Like: {current['apparentTemperature']} | "
                f"UV Index: {self.__uv_rating(current['uvIndex'])} |"
                f"High: {forecast_data[0]['temperatureHigh']}, Low: {forecast_data[0]['temperatureLow']} | "
                f"Humidity: {current['humidity']*100:.2f}% | "
                f"Sunrise: {sunrise}, "
                f"Sunset: {sunset} | "
                f"Today's Forecast: {forecast_data[0]['summary']}"
            )
            if 'alerts' in weather:
                result += " | Alerts: "
                result += ', '.join([x['title'] + ' ' + x['uri'] for x in weather['alerts']])
        elif kind == "hourly":
            result = f"{city}, {state} | {weather['hourly']['summary']} | "

            def h(x):
                hour = int(utils.unix_to_localtime(x['time'], tz=tz, fmt='%H'))
                day = utils.unix_to_localtime(x['time'], tz=tz, fmt='%a')
                return (
                  f"{hour} {x['summary']} "
                  f"{x['apparentTemperature']}F/"
                  f"{int(100 * x['humidity'])}%/"
                  f"{int(100 * x['precipProbability'])}%"
                )
            result += ' | '.join([h(hourly[x]) for x in range(0, kwargs['hours'])])
        else:
            raise Exception(f"Unknown type {kind}")


        return(result)
