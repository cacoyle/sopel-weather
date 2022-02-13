from . import darksky
from . import here
from . import utils
from . import irc
from . import shorturl

from functools import reduce

class WZ:
    UV=[irc.PLAIN] + [irc.GREEN] * 2 + [irc.YELLOW] * 3 + [irc.ORANGE] * 2 + [irc.RED] * 3 + [irc.PURPLE]

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

    def __short(self, url):
        short_url = shorturl.ShortenUrl(url)
        if short_url is not None
            return short_url
        return url


    def __uv_color(self, index):
        try:
            return WZ.UV[int(index)]
        except:
            return irc.PURPLE

    def __uv_rating(self, index):
        return f"{irc.COLOR}{self.__uv_color(index)}{index}{irc.RESET}"

    def __high(self):
        return f"{irc.COLOR}{irc.RED}↑{irc.RESET}"

    def __low(self):
        return f"{irc.COLOR}{irc.ROYAL_BLUE}↓{irc.RESET}"

    def __both(self, temp):
      temp_f = float(temp)
      temp_c = (5.0 / 9.0) * (temp_f - 32.0)
      return f"{int(temp_f):d}F/{temp_c:.2f}C"

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
        return getattr(self, f"get_{kind}")(city, state, weather, **kwargs)
        

    def get_forecast(self, city, state, weather, days):
        tz = weather['timezone']
        current = weather["currently"]
        forecast_data = weather["daily"]["data"]

        result = f"{city}, {state} Conditions: {current['summary']} | {weather['daily']['summary']} | "
        def f(i):
            fd = forecast_data[i]
            day = utils.unix_to_localtime(fd['time'], tz=tz, fmt='%a')
            high = self.__both(fd['temperatureHigh'])
            apparent_high = self.__both(fd['apparentTemperatureHigh'])
            low = self.__both(fd['temperatureLow'])
            apparent_low = self.__both(fd['apparentTemperatureLow'])
            return (
               f"{irc.BOLD}{day}{irc.RESET} "
               f"{self.__high()}{apparent_high} {self.__low()}{apparent_low} "
               f"{fd['summary']}"
            )
        result += ' | '.join([f(x) for x in range(0, days)])
        return result

    def get_current(self, city, state, weather):
        tz = weather['timezone']
        current = weather["currently"]
        forecast_data = weather["daily"]["data"]

        sunrise = utils.unix_to_localtime(forecast_data[0]['sunriseTime'], tz=tz)
        sunset = utils.unix_to_localtime(forecast_data[0]['sunsetTime'], tz=tz)
        temp = self.__both(current['temperature'])
        feel = self.__both(current['apparentTemperature'])
        high = self.__both(forecast_data[0]['temperatureHigh'])
        low = self.__both(forecast_data[0]['temperatureLow'])
        result = (
            f"{city}, {state} Conditions: {current['summary']} | "
            f"Temp: {temp}, Feels-Like: {feel} | "
            f"UV Index: {self.__uv_rating(current['uvIndex'])} | "
            f"{self.__high()}High: {high}, {self.__low()}Low: {low} | "
            f"Humidity: {current['humidity']*100:.2f}% | "
            f"Sunrise: {sunrise}, "
            f"Sunset: {sunset} | "
            f"Today's Forecast: {forecast_data[0]['summary']}"
        )
        if 'alerts' in weather:
            result += " | Alerts: "
            result += ', '.join([x['title'] + ' ' + self.__short(x['uri']) for x in weather['alerts']])
        return result

    def get_hourly(self, city, state, weather, hours):
        hourly = weather['hourly']['data']
        result = f"{city}, {state} | {weather['hourly']['summary']} | "
        tz = weather['timezone']

        def h(x):
            hour = int(utils.unix_to_localtime(x['time'], tz=tz, fmt='%H'))
            day = utils.unix_to_localtime(x['time'], tz=tz, fmt='%a')
            temp = self.__both(x['apparentTemperature'])
            return (
              f"{hour} {x['summary']} "
              f"{temp}/"
              f"{int(100 * x['humidity'])}%/"
              f"{int(100 * x['precipProbability'])}%"
            )
        result += ' | '.join([h(hourly[x]) for x in range(0, hours)])
        return result

    #def get_rain(self, city, state, weather):
    #    result = f"{city}, {state} | {weather['hourly']['summary']} | "
    #    hourly = weather['hourly']['data']
    #    groups = [0, 20, 40, 50, 60, 70, 80, 90, 100, 101]
    #    def get_group(percip):
    #        for i in range(1, len(groups)-1):
    #            if groups[i] >= percip:
    #                return i - 1
    #    import pdb; pdb.set_trace()

    #    def group(data, x):
    #        percip = int(100 * x['precipProbability'])
    #        g = get_group(percip)
    #        print(f"{percip}% {g}")
    #        if data[-1]['group'] == g:
    #            pass
    #        else:
    #            data.append({'group': g})
    #        return data
    #    data = reduce(group, hourly[1:], [{'group': get_group((100 * hourly[0]['precipProbability']))}])
    #    print(data)
    #    return(result)
