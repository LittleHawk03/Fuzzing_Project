from XSS import xssFuzz
from SQLi import scanSqlErrorBase
from WebConfig import web
import requests

def main():
    url = 'http://testphp.vulnweb.com/artists.php?artist=1'
    scanSqlErrorBase.scan(url)

    # html = web.getHTML(url,cookies={'PHPSESSID': '858cee892f7ee065d80e70f97e0c1303'})
    # html2 = web.getHTML('http://localhost:8080/vulnerabilities/xss_r/',cookies={'PHPSESSID': '858cee892f7ee065d80e70f97e0c1303'})
    # html = requests.post(url, data={'RequestVerificationToken': '<script>console.log(5000/3000)</script>'})
    # print(html)



if __name__ == '__main__':
    main()
