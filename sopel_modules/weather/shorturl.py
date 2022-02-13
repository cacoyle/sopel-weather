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

def ShortenUrl(url, default='Any', login='', apikey=''):
    api_service = ''
    result=url
    for attempt in range(MAX_ATTEMPTS):
        if ((attempt==0 and default=='Any') or default=='tinyurl'):
            url_data = {'url': url}
            api_service = 'http://tinyurl.com/api-create.php'
        elif (default=='is.gd'):
            url_data = {'format':'simple', 'url': url}
            api_service = 'http://is.gd/create.php'
        elif (default=='bitly'):
            url_data = {'format':'txt', 'login': login, 'apiKey': apikey, 'longUrl': url}
            api_service = 'http://api.bit.ly/v3/shorten'
        else:
            url_data = {'format':'simple', 'url': url}
            api_service = 'http://is.gd/create.php'
        short_url = ProcessUrl(api_service, url_data).strip()

        if (short_url[:4]=='http'):
            result=short_url
            break
    
    return result

def ProcessUrl(shorten_url, url_data):
    response = ''
    try_mobile_header=False
    query_string = urllib.parse.urlencode( url_data )
    shorten_url = shorten_url + "?" + query_string

    if (try_mobile_header==False):
        req = urllib.request.Request(url=shorten_url, data=None, headers=HEADERS)
    else:
        req = urllib.request.Request(url=shorten_url, data=None, headers=HEADERS_MOBILE)
    response = urllib.request.urlopen(req, timeout=5).read()
    return(response.decode('ascii'))
