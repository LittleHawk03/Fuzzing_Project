import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from threading import Thread
from WebConfig import web
from Logging import log as Log


class Crawler:
    visited_link = []
    unknown_link = []

    def __getLinks(self, host):
        link_to_visit = []
        res = web.getHTML(url=host)
        if res:
            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all('a', href=True):
                url = link['href']

                if urljoin(host, url) in self.visited_link:
                    continue
                elif url.startswith("mailto:") or url.startswith("javascript:") or url.startswith('<a href='):
                    continue
                elif url.startswith(host) or "://" not in url:
                    link_to_visit.append(urljoin(host, url))
                    print(f'\rCrawling ..... {str(len(self.visited_link))} url', end="\r")
                    self.visited_link.append(urljoin(host, url))
                else:
                    self.unknown_link.append(url)

            return link_to_visit
        else:
            return []

    def crawl(self, link, depth):
        urls = self.__getLinks(link)
        for url in urls:
            if url.startswith("https://") or url.startswith("http://"):
                if depth != 0:
                    t = Thread(target=self.crawl, args=(url, depth - 1,))
                    t.start()
                    t.join()
                else:
                    break
