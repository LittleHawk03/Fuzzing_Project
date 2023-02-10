from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from WebConfig import crawler
from Logging import log as Log
from FileInclusion import fileinclusion
import threading
import time
import argparse

def main():
    url = 'http://testphp.vulnweb.com/artists.php?artist=1'
    t = time.time()
    # rs = crawler.Crawler()
    # rs.crawl(url,1)
    # print(rs.table)
    t1 = threading.Thread(target=scanSqlErrorBase.scan,args=(url,1))
    t2 = threading.Thread(target=xssFuzz.scan_xss,args=(url,1))
    t3 = threading.Thread(target=fileinclusion.scaner_file_inclusion,args=(url,))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    Log.info('time : ' + str(time.time()  - t))

    t2 = time.time()
    scanSqlErrorBase.scan(url,1)
    xssFuzz.scan_xss(url,1)
    fileinclusion.scaner_file_inclusion(url)
    Log.info('time : ' + str(time.time() - t2))

if __name__ == '__main__':
    main()
