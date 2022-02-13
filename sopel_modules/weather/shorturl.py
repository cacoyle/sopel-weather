# -*- coding: utf-8 -*-
# URL shortener using short url services.
# Created By Abdul Hamid
# 06 March 2014
# ah@appscluster.com

import sys, time, os.path, getopt, socket
import urllib, urllib.parse, urllib.error, urllib.request

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'}
HEADERS_MOBILE = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}

MAX_ATTEMPTS = 3
VERSION = '0.0.4'

SERVICES = {
    'is.gd': {'host': 'http://is.gd/create.php', 'url': lambda url: {'format':'simple', 'url': url}},
    'tinyurl': {'host': 'http://tinyurl.com/api-create.php', 'url': lambda url: {'url': url}}
}


def ShortenUrl(url):
    result = None
    for _, service in SERVICES.items():
      api_service = service['host']
      url_data = service['url'](url)
      try:
        short_url = ProcessUrl(api_service, url_data, False).strip()
      except (urllib.error.URLError, socket.timeout) as e:
        try:
          short_url = ProcessUrl(api_service, url_data, True).strip()
        except (urllib.error.URLError, socket.timeout) as e:
          continue

      if (short_url[:4]=='http'):
          result=short_url
          break
    
    return result

def ProcessUrl(shorten_url, url_data, try_mobile_header=False):
    response = ''
    query_string = urllib.parse.urlencode( url_data )
    shorten_url = shorten_url + "?" + query_string
    headers = HEADERS if try_mobile_header==False else HEADERS_MOBILE
    req = urllib.request.Request(url=shorten_url, data=None, headers=headers)
    response = urllib.request.urlopen(req, timeout=5).read()
    return(response.decode('ascii'))
