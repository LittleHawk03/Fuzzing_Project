from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from WebConfig import crawler

def main():
    url = 'http://localhost:9991/SQL/sql1.php'
    # rs = crawler.Crawler()
    # rs.crawl(url,1)
    # print(rs.table)
    scanSqlErrorBase.scan(url,0)
    # xssFuzz.check(url)
    # html = web.getHTML(url,cookies={'PHPSESSID': '858cee892f7ee065d80e70f97e0c1303'})
    # html2 = web.getHTML('http://localhost:8080/vulnerabilities/xss_r/',cookies={'PHPSESSID': '858cee892f7ee065d80e70f97e0c1303'})
    # html = requests.post(url, data={'RequestVerificationToken': '<script>console.log(5000/3000)</script>'})
    # print(html)



if __name__ == '__main__':
    main()
