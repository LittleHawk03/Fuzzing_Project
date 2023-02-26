import Logging
from Logging import log as Log
import requests
from urllib.error import HTTPError, URLError, ContentTooShortError
from urllib.parse import urlparse
import socket
from WebConfig import useragents

"""
    Mình xây dựng module này để thiết lập request nó có các sử lý ngoại lệ và trả về False nếu request hỏng
    còn nếu không thì nó sẽ trả về giá trị để mình phân tich
"""


def getHTML(url, lastUrl=False, method=None, headers=None, data=None, params=None, verify=None, cookies=None):
    if method is None:
        method = 'get'

    if not (url.startswith("http://") or url.startswith("https://")):
        url = 'http://' + url

    if headers is None:
        headers = useragents.get()

    html = None

    try:
        if method == 'get':
            req = requests.get(url, headers=headers, cookies=cookies, params=params, verify=verify, timeout=2000)
            # Log.info('url : ' + str(req.url))
        else:
            req = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=2000)
            # Log.info('url : ' + req.url)
    except requests.exceptions.HTTPError as http:
        Log.error('something wrong with http request')
    except requests.exceptions.InvalidURL as urlError:
        Log.error('something wrong with url')
    except requests.exceptions.Timeout:
        Log.error('time out')
    except requests.exceptions.TooManyRedirects:
        Log.error('URL was bad and try a different one')
    except Exception as e:
        Log.error("error " + str(e))
    else:
        html = req

    if html:
        if lastUrl:
            return html, req.url
        else:
            return html

    return False
