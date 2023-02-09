from WebConfig import crawler
# from bs4 import BeautifulSoup
# from WebConfig import web
# import requests
# from urllib.parse import urlparse, urljoin
# from SQLi import sqlerrors
# from XSS import xssFuzz


def main():
    # xssFuzz.post_method()
    url = 'http://localhost:9991/SQL/sql1.php'
    # myhtml = requests.get(url)
    # print(sqlerrors.check(myhtml.text))
    rs = crawler.Crawler()
    rs.crawl(url, 2)
    print(rs.visited_link)
    print("crawler success")

    # domain = url.split("?")[0]  # domain with path without queries
    # queries = urlparse(url).query.split("&")
    # # payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
    # flag = 0
    #
    # for payload in payloads:
    #     website = domain + "?" + ("&".join([param + payload for param in queries]))
    #     print(website)
    #     source = web.getHTML(website, False)
    #     print('scanning : ' + website)
    #     print(source)
    #     if source:
    #         vulnerable, db = sqlerrors.check(source)
    #         print(vulnerable)
    #         if vulnerable and db is not None:
    #             print('[+] {} vulnerable'.format(url))
    #             flag = 1
    #             # break
    #         else:
    #             print('[+] {} safe'.format(url))




if __name__ == '__main__':
    main()
