from urllib.parse import urljoin, urlparse, urlencode, parse_qs
from bs4 import BeautifulSoup
from Logging import log as Log
from WebConfig import web
from XSS import generratePayload

f = open("XSS/xss.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())


def scan_form_in_url(url,vulnerable_url , cookies=None):
    html = web.getHTML(url, cookies=cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    forms = soup.find_all('form', method=True)

    for form in forms:
        # kiểm tra action hay còn gọi là phần query của một url ví dụ /account/login
        try:
            action = form['action']
        except KeyError:
            action = url

        try:
            print('method : ' + form['method'])
            method = form['method'].lower().strip()
        except KeyError:
            method = 'get'

        for payload in payloads:
            keys = {}
            for key in form.find_all(["input", "textarea"]):

                try:
                    if key['type'] == 'submit':
                        keys.update({key['name']: key['name']})
                    else:
                        keys.update({key['name']: payload})
                except Exception as e:
                    Log.warning('Internal error: ' + str(e))
                    if method.lower().strip() == 'get':
                        try:
                            keys.update({key['name']: payload})
                        except KeyError as e:
                            Log.info("Internal error: " + str(e))

            # bat dau set requests (manh duc)
            final_url = urljoin(url, action)
            if method.lower().strip() == 'get':
                req_html = web.getHTML(final_url, method=method.lower(), params=keys, cookies=cookies)
                if payload in req_html.text:
                    Log.high(Log.R + ' Vulnerable deteced in url :' + final_url)
                    vulnerable_url.append([final_url, 'form', payload])
                    break
            elif method.lower().strip() == 'post':
                req_html = web.getHTML(final_url, method=method.lower(), data=keys, cookies=cookies)
                if payload in req_html.text:
                    Log.high(Log.R + ' Vulnerable deteced in url :' + final_url)
                    vulnerable_url.append([final_url, 'form', payload])
                    break


def scan_all_link_in_url(url, vulnerable_url,cookies=None):
    html = web.getHTML(url, cookies=cookies)
    # print(html)
    soup = BeautifulSoup(html.text, 'html.parser')
    links = soup.find_all('a', href=True)

    for a in links:

        host = a['href']
        # ('host = ' + host)
        if 'http://' not in host or 'https://' not in host or 'mailto:' not in host:
            base = urljoin(url, host)
            query = urlparse(base).query
            if query != '':
                for payload in payloads:
                    Log.info('find the query in url : ' + str(query))
                    query_payload = query.replace(query[query.find('=') + 1:len(query)], payload, 1)
                    check_url = base.replace(query, query_payload, 1)
                    Log.info('check_url : ' + check_url)
                    Log.info('parse query' + str(parse_qs(query)))
                    Log.info('encode query : ' + str(urlencode({x: payload for x in parse_qs(query)})))
                    check_url_query_all = base.replace(query, urlencode({x: payload for x in parse_qs(query)}))
                    Log.info('check_url_query_all : ' + str(check_url_query_all))
                    if not host.startswith("mailto:") and not host.startswith("tel:"):
                        req_1 = web.getHTML(check_url, verify=False)
                        req_2 = web.getHTML(check_url_query_all)
                        if payload in req_1.text or payload in req_2.text:
                            Log.high(Log.R + ' Vulnerable deteced in url :' + check_url_query_all)
                            vulnerable_url.append([check_url, 'url/href', payload])
                            break


def scan_in_a_url(url, vulnerable_url ,cookies=None):
    query = urlparse(url).query
    if query != '':
        for payload in payloads:
            Log.info('find the query in url : ' + str(query))
            query_payload = query.replace(query[query.find('=') + 1:len(query)], payload, 1)
            check_url = url.replace(query, query_payload, 1)
            Log.info('check_url : ' + check_url)
            Log.info('parse query' + str(parse_qs(query)))
            Log.info('encode query : ' + str(urlencode({x: payload for x in parse_qs(query)})))
            check_url_query_all = url.replace(query, urlencode({x: payload for x in parse_qs(query)}))
            Log.info('check_url_query_all : ' + str(check_url_query_all))
            if not url.startswith("mailto:") and not url.startswith("tel:"):
                req_1 = web.getHTML(check_url, verify=False)
                req_2 = web.getHTML(check_url_query_all)
                if payload in req_1.text or payload in req_2.text:
                    Log.high(Log.R + ' Vulnerable deteced in url :' + check_url_query_all)
                    vulnerable_url.append([check_url, 'form', payload])
                    return True, [check_url, 'url/href', payload]
        return False
    return False


def scan_xss(url, method=2, cookies=None):
    vulnerable_url = []
    if method >= 2:
        scan_in_a_url(url,vulnerable_url)
        scan_form_in_url(url,vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
    elif method == 1:
        scan_in_a_url(url,vulnerable_url)
        scan_form_in_url(url,vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
    elif method == 0:
        scan_form_in_url(url,vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
