# sopel-weather
Weather module for sopel. 


## Requirements
* [Darksky API account](https://darksky.net/dev)
* [Here.com API account](https://developer.here.com/?cid=www.here.com-main_menu)


## Installation
* copy wz.py to `~/.sopel/modules`, or whatever path your sopel installation resides in.
* Set the values for `here_app_id`, `here_app_code`, and `darksky_key`
* Restart sopel


## Usage
### Via bot
* `.wz <zip code>`


### Via script or REPL
```
>>> # You'll need sopel.module installed in your environment
>>> from wz import get_temp_by_zip 
>>>
>>> get_temp_by_zip(90210) 
"Beverly Hills, CA Conditions: Mostly Cloudy | Temp: 65.46F | High: 66.58F, Low: 58.43F | Humidity: 77.00% | Sunrise: 08:44:56, Sunset: 23:10:08 | Today's Forecast: Mostly cloudy throughout the day." 
```
