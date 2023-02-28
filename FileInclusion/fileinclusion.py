from WebConfig import web
from Logging import log as Log
from urllib.parse import urlparse, urljoin

f = open("FileInclusion/fileic.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())

KEYS_WORDS = ["root:x:0:0", "root:/root:", "daemon:x:1:", "daemon:x:2", "bin:x:1:1"
    , "/bin/bash", "/sbin/nologin", "man:x:", "mail:x:", "games:x:", "Nobody:"
    , "MySQL Server", "gnats:x:", "www-data:x:", "/usr/sbin/", "backup:x:"]


"""
Dựa vào kết quả thông báo lỗi của hệ thống
ta có thể biết được hệ thống có thực thi đoạn
dữ liệu fuzzing đầu vào hay không hoặc
URL đó có tồn tại hay không.
Ví dụ: Khi tìm một URL mặc định của hệ
thống. Nếu nó trả về giá trị lớn hơn hoặc
bằng 200 và nhỏ hơn 300. Thì có nghĩa là
URL đó là tồn tại.

"""

def find_key_words(html):
    for key_word in KEYS_WORDS:
        if key_word in html:
            return True
    return False


def scaner_file_inclusion(url, vulnerable_url):
    querys = urlparse(url).query
    Log.info("scan file inclusion : " + url)
    for payload in payloads:
        # chèn payload vào query trong các urltồn tại query ví dụ: https://manhduc/name=1
        # + /etc/pass -> https: // manhduc / name = / etc / passwd
        if querys != '':
            parser_query = []
            for query in querys.split("&"):
                parser_query.append(query[0:query.find('=') + 1])
            new_query = "&".join([que + payload for que in parser_query])
            new_url = url.replace(querys, new_query, 1)
        #sử dụng để gộp url ví dụ https://manhduc/ + /etc/pass -> https://manhduc/etc/passwd
            source = web.getHTML(new_url)
            if source:
                if find_key_words(source.text) or (200 <= source.status_code <= 299):
                    # print(source.text)
                    Log.high(Log.R + ' Vulnerable detected in url :' + new_url)
                    vulnerable_url.append([new_url, 'url/href','file inclution', payload])
                    return True

        return False
