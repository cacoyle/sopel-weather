from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import commands, example
from sopel import web
from .wz import WZ

import sopel.module

class WeatherSection(StaticSection):
    here_url = ValidatedAttribute('here_url', default="https://geocoder.api.here.com/6.2/geocode.json")
    here_app_id = ValidatedAttribute('here_app_id', default=None)
    here_app_code = ValidatedAttribute('here_app_code', default=None)
    darksky_url = ValidatedAttribute("darksky_url", default="https://api.darksky.net/forecast")
    darksky_key = ValidatedAttribute("darksky_key", default=None)

def configure(config):
    config.define_section('weather', WeatherSection, validate=False)
    config.weather.configure_setting('here_url', 'here.com api url')
    config.weather.configure_setting('here_app_id', 'here.com app id')
    config.weather.configure_setting('here_app_code', 'here.com app code')
    config.weather.configure_setting('darksky_url', 'darksky.com api url')
    config.weather.configure_setting('darksky_key', 'darksky.com id')

def setup(bot):
    bot.config.define_section('weather', WeatherSection)

def check(bot, trigger):
    msg = None
    if not bot.config.weather.here_url:
        msg = 'Weather API here.com url not configured.'
    elif not bot.config.weather.here_app_id:
        msg = 'Weather API here.com app id not configured.'
    elif not bot.config.weather.here_app_code:
        msg = 'Weather API here.com app code not configured.'
    elif not bot.config.weather.darksky_url:
        msg = 'Weather API darksky.com url not configured.'
    elif not bot.config.weather.darksky_key:
        msg = 'Weather API darksky.com key not configured.'
    elif not trigger.group(2):
        msg = 'You must provide a query.'
    return msg

@sopel.module.commands('wz')
@sopel.module.example('.wz 90210')
@sopel.module.example('.wz Los Vegas, NV')
def weatherbot_current(bot, trigger):
  msg = check(bot, trigger)
  if not msg:
      wz = WZ(
              bot.config.weather.here_url,
              bot.config.weather.here_app_id,
              bot.config.weather.here_app_code,
              bot.config.weather.darksky_url,
              bot.config.weather.darksky_key)
      msg = wz.get(trigger.group(2))
  bot.say(msg)

@sopel.module.commands('wzf')
@sopel.module.example('.wzf 90210')
@sopel.module.example('.wzf Los Vegas, NV')
def weatherbot_forecast(bot, trigger):
  msg = check(bot, trigger)
  if not msg:
      wz = WZ(
              bot.config.weather.here_url,
              bot.config.weather.here_app_id,
              bot.config.weather.here_app_code,
              bot.config.weather.darksky_url,
              bot.config.weather.darksky_key)
      msg = wz.get(trigger.group(2), forecast=True)
  bot.say(msg)
