from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from WebConfig import crawler,crawler2,web
from Logging import log as Log
from FileInclusion import fileinclusion
from threading import Thread
import time
from prettytable import PrettyTable
import argparse


def crawler_url(url, level=1):
    cr = crawler2.Crawler()
    cr.crawl(url, level)
    cr.visited_link.append(url)
    return cr.visited_link


def crawler_and_check_sqlI(url, vulnerable_url, cr,level=1):
    threads = []
    # cr = crawler_url(url, level)
    for url in cr:
        t = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_url, args=(url, vulnerable_url,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        # t.join()


def crawler_and_check_xss(url, vulnerable_url, cr,level=1):
    threads = []
    # cr = crawler_url(url,level=level)
    for url in cr:
        t = Thread(target=xssFuzz.scan_form_in_url, args=(url, vulnerable_url))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def crawler_and_check_fileI(url, vulnerable_url, cr):
    threads = []
    # cr = crawler_url(url)
    for url in cr:
        t = Thread(target=fileinclusion.scaner_file_inclusion,args=(url, vulnerable_url))
        t.start()

    for thread in threads:
        thread.join()

def main():
    url = 'http://localhost:9991/XSS/XSS_level1.php'
    vul = []
    scanSqlErrorBase.scan_sql_error_base_in_form(url,vul)
    # t = time.time()
    # vulnerable_url = []
    # cr = crawler_url(url, 2)
    # t1 = Thread(target=crawler_and_check_sqlI, args=(url, vulnerable_url,cr, 2))
    # t2 = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_form, args=(url, vulnerable_url))
    # t3 = Thread(target=crawler_and_check_xss, args=(url, vulnerable_url,cr, 2))
    # t4 = Thread(target=xssFuzz.scan_form_in_url, args=(url, vulnerable_url))
    # t5 = Thread(target=crawler_and_check_fileI, args=(url, vulnerable_url,cr,))
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    #
    # table = PrettyTable()
    # table.add_rows(vulnerable_url)
    # print(table)
    # Log.info('time : ' + str(time.time() - t))

    # t2 = time.time()
    # scanSqlErrorBase.scan(url,1)
    # xssFuzz.scan_xss(url,1)
    # fileinclusion.scaner_file_inclusion(url)
    # Log.info('time : ' + str(time.time() - t2))


if __name__ == '__main__':
    main()
