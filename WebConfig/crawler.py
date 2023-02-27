import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from WebConfig import web

"""
    cái class này dùng để cào các ủrl về nhá 
    thì các url hay các đường dẫn thường đặt trong các thẻ href trong html href='/account/log'
    thế nên để cào được dữ liệu thì mình chỉ cần lấy giá trị thẻ href rồi gộp vào url chính thông quan urljoin()
    urljoin('https://ducdeptrai/','/account/log') = https://ducdeptrai/account/log

"""


class Crawler:
    visited_link = []
    unknown_link = []

    def __getLinks(self, host):
        link_to_visit = []
        res = web.getHTML(url=host)
        soup = BeautifulSoup(res.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            """ link['href'] = 'http://www.acunetix.com'"""
            url = link['href']
            """ http://testphp.vulnweb.com/privacy.com"""
            if urljoin(host, url) in self.visited_link:
                continue
            elif url.startswith("mailto:") or url.startswith("javascript:") or url.startswith('<a href='):
                continue
            elif url.startswith(host) or "://" not in url:
                print(urljoin(host, url))
                link_to_visit.append(urljoin(host, url))
                self.visited_link.append(urljoin(host, url))
            else:
                self.unknown_link.append(url)

        return link_to_visit


"""
dùng đệ quy để tiến hành cào sâu vào trong mỗi url
"""


def crawl(self, link, depth):
    urls = self.__getLinks(link)
    for url in urls:
        if url.startswith("https://") or url.startswith("http://"):
            if depth != 0:
                self.crawl(url, depth - 1)
            else:
                break


