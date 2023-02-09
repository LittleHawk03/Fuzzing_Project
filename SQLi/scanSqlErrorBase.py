from urllib.parse import urlparse, urljoin, urlencode, parse_qs

from bs4 import BeautifulSoup
import time
from Logging import log as Log
from SQLi import sqlerrors
from WebConfig import web

f = open("sql.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())


def scan_sql_error_base_in_form(url, vulnerable_url):
    html = web.getHTML(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    forms = soup.find_all('form', method=True)
    Log.info('request : ' + url + " in form with action")
    for form in forms:
        try:
            action = form['action']
        except KeyError:
            action = url
        try:
            method = form['method'].lower().strip()
        except KeyError:
            method = 'get'

        for payload in payloads[:30]:
            keys = {}
            for key in form.find_all(["input", "textarea"]):
                try:
                    if key['type'] == 'submit':
                        keys.update({key['name']: key['name']})
                    else:
                        keys.update({key['name']: payload})
                except Exception as e:
                    Log.error("Internal error " + str(e))
            final_url = urljoin(url, action)
            if method == 'get':
                source = web.getHTML(final_url, method=method, params=keys)
                vulnerable, db = sqlerrors.check(source.text)
                if vulnerable and (db is not None):
                    vulnerable_url.append([final_url, 'form', payload])
                    Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url)
                    break
            elif method == 'post':
                source = web.getHTML(final_url, method=method, data=keys)
                print(source.text)
                vulnerable, db = sqlerrors.check(source.text)
                if vulnerable and (db is not None):
                    vulnerable_url.append([final_url, 'form', payload])
                    Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url)
                    break


def scan_sql_error_base_in_url(url, vulnerable_url):
    # cái này để lấy url thuần mà không có phần query
    queries = urlparse(url).query
    for payload in payloads:
          # lấy phần queries trong url ra
        if queries != '':
            parser_query = []
            for query in queries.split("&"):
                parser_query.append(query[0:query.find('=') + 1])

            query = "&".join([param + payload for param in parser_query])

            encode_query = urlencode({x: payloads for x in parse_qs(queries)})

            final_url = url.replace(queries, query, 1)

            final_encode_url = url.replace(queries, encode_query, 1)

            source = web.getHTML(final_url)
            source_encode = web.getHTML(final_encode_url)

            if source :
                vulnerable1, db1 = sqlerrors.check(source.text)
                vulnerable2, db2 = sqlerrors.check(source_encode.text)
                if (vulnerable1 and (db1 is not None)) or (vulnerable2 and (db1 is not None)):
                    Log.high(Log.R + ' Vulnerable deteced in url :' + final_url)
                    vulnerable_url.append([final_url, 'url/href', payload])
                    return True
    return False


def scan(url, method=2):
    vulnerable_url = []
    if method >= 2:
        t = time.time()
        scan_sql_error_base_in_url(url, vulnerable_url)
        scan_sql_error_base_in_form(url, vulnerable_url)
        if len(vulnerable_url):
            print('time : ' + str(time.time() - t))
            print(vulnerable_url)
            return True, vulnerable_url
        else:
            return False
    elif method == 1:
        scan_sql_error_base_in_url(url, vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
    elif method == 0:
        scan_sql_error_base_in_form(url, vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False

