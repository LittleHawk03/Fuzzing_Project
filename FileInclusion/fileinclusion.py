from WebConfig import web
from Logging import log as Log
from urllib.parse import urlparse

f = open("fileic.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())


KEYS_WORDS = ["root:x:0:0","root:/root:","daemon:x:1:","daemon:x:2","bin:x:1:1"
                ,"/bin/bash","/sbin/nologin","man:x:","mail:x:","games:x:","Nobody:"
                ,"MySQL Server","gnats:x:","www-data:x:","/usr/sbin/","backup:x:"]

def find_key_words(html):
    for key_word in KEYS_WORDS:
        if key_word in html:
            return True
    return False


def scaner_file_inclusion(url):
    querys = urlparse(url).query
    for payload in payloads:
        if querys != '':
            parser_query = []
            for query in querys.split("&"):
                parser_query.append(query[0:query.find('=') + 1])

            new_query = "&".join([que + payload for que in parser_query])
            new_url = url.replace(querys,new_query,1)
            source = web.getHTML(new_url)
            if source and source.status_code == 200:
                if find_key_words(source.text):
                    print(source.text)
                    Log.high(Log.R + ' Vulnerable deteced in url :' + new_url)
                    return True
    return False
