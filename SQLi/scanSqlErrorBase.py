from urllib.parse import urlparse, urljoin, urlencode, parse_qs

from bs4 import BeautifulSoup
import time
from Logging import log as Log
from SQLi import sqlerrors
from WebConfig import web

f = open("SQLi/sql.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())

"""
 scan_sql_error_base_in_form(url, vulnerable_url) :
 hàm này dùng để scan các lỗi sql inject thông qua thẻ <form> trong html
 ví dụ nhá : 
 <form action="search.php?test=query" method="post"> 
      <label>search art</label> 
      <input name="searchFor" type="text" size="10"> 
      <input name="goButton" type="submit" value="go"> 
</form>

    thì để request trong python với một form như này module requests sẽ yêu cầu chuyền vào 
    tham số data={} (dạng dictionary)
    
    ví dụ như trong form trên thì requests yêu cầu data/param sẽ là {"searchFor":"duc buoi to","goButton":"goButton"}
    với logic như thế mình sẽ chèn payload vào form với dạng như sau {"searchFor":"-1 or 1=1 --","goButton":"goButton"}
    
    với hàm này ta sử dụng hàm BeautifulSoup để phân tích html nó sẽ phân tích html ra các thẻ và để tìm kiếm các thẻ ta 
    sử dụng hàm find_all
    ví dụ nhá :
    soup = BeautifulSoup(html.text, 'html.parser')
    forms = soup.find_all('form', method=True)
    còn cái bên dưới này là để lấy các giá trị trả về từ module requests
    html = web.getHTML(url) 
"""


def scan_sql_error_base_in_form(url, vulnerable_url):
    html = web.getHTML(url)  ## lấy giá trị được trả về từ module request
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
                    """nếu như type trong form là submit thì {name : name} nha sẽ có vẫn đề xẩy ra đó"""
                    if key['type'] == 'submit':
                        keys.update({key['name']: key['name']})
                    else:
                        keys.update({key['name']: payload})
                except Exception as e:
                    Log.error("Internal error " + str(e))
                    # if str(e) == 'name':
                    keys.update({key['value']: key['value']})

            print(keys)
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


"""
scan_sql_error_base_in_url(url, vulnerable_url):
    hàm này sẽ là hàm chính để tìm kiếm lỗi này đọc rõ nghen 
    như này nhá :
    - thì một url như này https://manhducyeutatcacacem.com//?id=1 thì sẽ có các thành phần 
    id=1 thành phần này gọi là query dùng để đưa dữ liệu cần tìm kiếm vào để tìm kiếm như ở đây nó sẽ tìm những thằng có id bằng 1
    theo cách này ta tìm cách  đẩy các dữ liệu không hợp lê (payload) vào cái thành phần query này 
    - để có thể tách được thành phần query này ra khỏi url thì mình dùng urlparse từ module urllib.parse
    ví dụ : queries = urlparse(url).query -> nó sẽ tách thành phần url thành id=1
    - ờm dcm thì sau khi tách được id=1 thì mình chèn payload vào nhá như này id=-1 or 1=1--
    - rồi để có thể kiểm tra được thì ta sẽ phải nối thành phần url với thành phần query như này :
    https://manhducyeutatcacacem.com/ +  id=-1 or 1=1-- -> https://manhducyeutatcacacem.com/?id=-1 or 1=1--
    - rồi sau đó mình request cái url để lấy html trả về nếu có thông báo lỗi là thôi rồi lượm ơi nó có thể có lỗi sql injection
"""


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

