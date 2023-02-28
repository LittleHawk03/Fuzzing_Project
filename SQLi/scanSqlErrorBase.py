from urllib.parse import urlparse, urljoin, urlencode, parse_qs

from bs4 import BeautifulSoup
import time
from Logging import log as Log
from Logging import progressBar
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
    
    ví dụ như trong form trên thì requests yêu cầu data/param sẽ là {"searchFor":"duc dep trai","goButton":"goButton"}
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
    html = web.getHTML(url)
    ## lấy giá trị được trả về từ module request

    if html:
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
            i = 0
            for payload in payloads[:30]:
                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        """nếu như type trong form là submit thì {name : name} nha nhưng sẽ có vẫn đề xẩy ra đó"""
                        if key['type'] == 'submit':
                            try:
                                keys.update({key['name']: key['name']})
                            except Exception as e:
                                keys.update({key['value']: key['value']})
                        else:
                            keys.update({key['name']: payload})
                    except Exception as e:
                        Log.error("Internal error " + str(e))

                final_url = urljoin(url, action)
                Log.info('target url/form : ' + final_url)
                if method == 'get':
                    source = web.getHTML(final_url, method=method, params=keys)
                    vulnerable, db = sqlerrors.check(source.text)
                    if vulnerable and (db is not None):
                        vulnerable_url.append([final_url, 'form','sqli', payload])
                        Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url + ']')
                        # progressBar.progressbar(30, 30, prefix='Progress:', suffix='Complete', length=50)
                        break
                elif method == 'post':
                    source = web.getHTML(final_url, method=method, data=keys)
                    vulnerable, db = sqlerrors.check(source.text)
                    if vulnerable and (db is not None):
                        vulnerable_url.append([final_url, 'form','sqli', payload])
                        Log.high(Log.R + ' Vulnerable deteced in url/form :' + final_url)
                        # progressBar.progressbar(30, 30, prefix='Progress:', suffix='Complete', length=50)
                        break
                progressBar.progressbar(i + 1,30,prefix = 'Progress:', suffix = 'Complete', length = 50)
                i +=1


"""
scan_sql_error_base_in_url(url, vulnerable_url):
    hàm này sẽ là hàm chính để tìm kiếm lỗi này đọc rõ nghen 
    như này nhá :
    - thì một url như này https://manhducdeptrai.com//?id=1 thì sẽ có các thành phần 
    id=1 thành phần này gọi là query dùng để đưa dữ liệu cần tìm kiếm vào để tìm kiếm như ở đây nó sẽ tìm những thằng có id bằng 1
    theo cách này ta tìm cách  đẩy các dữ liệu không hợp lê (payload) vào cái thành phần query này 
    - để có thể tách được thành phần query này ra khỏi url thì mình dùng urlparse từ module urllib.parse
    ví dụ : queries = urlparse(url).query -> nó sẽ tách thành phần url thành id=1
    - ờm thì sau khi tách được id=1 thì mình chèn payload vào nhá như này id=-1 or 1=1--
    - rồi để có thể kiểm tra được thì ta sẽ phải nối thành phần url với thành phần query như này :
    https://manhducdeptrai.com/ +  id=-1 or 1=1-- -> https://manhducdeptraideptrai.com/?id=-1 or 1=1--
    - rồi sau đó mình request cái url để lấy html trả về nếu có thông báo lỗi là thôi rồi lượm ơi nó có thể có lỗi sql injection
"""


def scan_sql_error_base_in_url(url, vulnerable_url):


    # cái này để lấy url thuần mà không có phần query

    Log.info('target url : ' + url)
    """
     https://example.com ? name=1&id=2
    """
    queries = urlparse(url).query
    '''
    queries = name=1&id=2
    '''
    i = 0
    for payload in payloads:
          # lấy phần queries trong url ra
        if queries != '':
            parser_query = []
            '''queries.split("&") = ['name=1','id=2']'''
            for query in queries.split("&"):
                parser_query.append(query[0:query.find('=') + 1])
            ''' parser_query = ['name=','id='] '''
            new_query = "&".join([param + payload for param in parser_query])
            ''' query = 'name=[payload]&id=[payload]' '''
            final_url = url.replace(queries, new_query, 1)

            """cách 2"""
            encode_query = urlencode({x: payloads for x in parse_qs(queries)})
            final_encode_url = url.replace(queries, encode_query, 1)
            # source = web.getHTML(final_url)
            res = web.getHTML(final_encode_url)

            if res:
                # vulnerable1, db1 = sqlerrors.check(source.text)
                vulnerable2, db2 = sqlerrors.check(res.text)
                if vulnerable2 and (db2 is not None):
                    Log.high(Log.R + ' Vulnerable sqli deteced in url :' + final_url)
                    vulnerable_url.append([final_url, 'url/href','sqli', payload])
                    progressBar.progressbar(30, 30, prefix='Progress:', suffix='Complete', length=0)
                    return True
            progressBar.progressbar(i + 1,len(payloads), prefix='Progress:', suffix='Complete', length=50)
            i += 1
        else:
            return False
    return False





"""cái này dùng để test """
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

