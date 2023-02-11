import argparse
import threading

from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from FileInclusion import fileinclusion
from WebConfig import crawler, crawler2
from prettytable import PrettyTable
from threading import Thread
from Logging import log as Log
import time

picture = Log.G + """
████████████████████████████████████████████████████████████████████████████████
█░░░░░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░██░░░░░░░░█
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░█
█░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░░░█░░░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░█████████░░▄▀░░███████████░░▄▀▄▀░░▄▀▄▀░░███
█░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░░░███░░░░▄▀▄▀▄▀░░░░███
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█████░░░░▄▀░░░░█████
█░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀░░█░░░░░░░░░░▄▀░░█░░░░░░░░░░▄▀░░███████░░▄▀░░███████
█░░▄▀░░█████████░░▄▀░░██░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░███████░░▄▀░░███████
█░░▄▀░░█████████░░▄▀░░░░░░▄▀░░█░░░░░░░░░░▄▀░░█░░░░░░░░░░▄▀░░███████░░▄▀░░███████
█░░▄▀░░█████████░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░███████░░▄▀░░███████
█░░░░░░█████████░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░███████░░░░░░███████
████████████████████████████████████████████████████████████████████████████████"""


def crawler_url(url, level=1):
    cr = crawler2.Crawler()
    cr.crawl(url, level)
    cr.visited_link.append(url)
    return cr.visited_link


def crawler_and_check_sqlI(url, vulnerable_url, level=1):
    threads = []
    cr = crawler_url(url, level)
    for url in cr:
        t = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_url, args=(url, vulnerable_url,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        # t.join()


def crawler_and_check_xss(url, vulnerable_url,level=1):
    threads = []
    cr = crawler_url(url,level=level)
    for url in cr:
        t = Thread(target=xssFuzz.scan_in_a_url, args=(url, vulnerable_url))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def crawler_and_check_fileI(url, vulnerable_url):
    threads = []
    cr = crawler_url(url)
    for url in cr:
        t = Thread(target=fileinclusion.scaner_file_inclusion,args=(url, vulnerable_url))
        t.start()

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="target url for scanning", type=str, dest='target')
    parser.add_argument('-c', '--crawler', help="the option for auto crawler from a url", default=2,action='store_true', dest='crawler')
    parser.add_argument('-s', '--sql', help="auto detect a sql injection from a url", action='store_true', dest='sql')
    parser.add_argument('-x', '--xss', help="auto detect a sxx vulnerable from a url", action='store_true', dest='xss')
    parser.add_argument('-f', '--file', help="auto detect a file inclusion from a url", action='store_true', dest='file')
    parser.add_argument('-a' '--auto', help="auto crawler an scanner all url after crawler url form a website", action='store_true', dest='auto')
    parser.add_argument('-ps', '--payloadsqli', help="show all payload of sql injection", action='store_true', dest='ps')
    parser.add_argument('-px', '--payloadxss', help="show all payload of xss vulnerable", action='store_true', dest='px')
    args = parser.parse_args()
    if args.target is not None and args.sql:
        t = time.time()
        vulnerable_url = []
        t1 = Thread(target=crawler_and_check_sqlI, args=(args.target, vulnerable_url,))
        t2 = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_form, args=(args.target, vulnerable_url))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        table = PrettyTable()
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.xss:
        t = time.time()
        vulnerable_url = []
        t1 = Thread(target=crawler_and_check_xss, args=(args.target, vulnerable_url,))
        t2 = Thread(target=xssFuzz.scan_form_in_url, args=(args.target, vulnerable_url,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        table = PrettyTable()
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.file:
        t = time.time()
        vulnerable_url = []
        t1 = Thread(target=crawler_and_check_fileI, args=(args.target, vulnerable_url,))
        t1.start()
        t1.join()
        table = PrettyTable()
        table.add_rows(vulnerable_url)
        print(table)
    elif args.target is not None and args.auto:
        t = time.time()
        vulnerable_url = []
        t1 = Thread(target=crawler_and_check_sqlI, args=(args.target, vulnerable_url, 2))
        t2 = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_form, args=(args.target, vulnerable_url))
        t3 = Thread(target=crawler_and_check_xss, args=(args.target, vulnerable_url, 2))
        t4 = Thread(target=xssFuzz.scan_form_in_url, args=(args.target, vulnerable_url,))
        t5 = Thread(target=crawler_and_check_fileI, args=(args.target, vulnerable_url,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

        table = PrettyTable()
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.crawler:
        t = time.time()
        cr = crawler2.Crawler()
        cr.crawl(args.target, args.crawler)
        cr.visited_link.append(args.target)
        print(cr.visited_link)
        Log.info('time : ' + str(time.time() - t))
    elif args.ps:
        f = open("SQLi/sql.txt", "r")
        for pay in f.readlines():
            print(pay)
    elif args.px:
        f = open("XSS/xss.txt", "r")
        for pay in f.readlines():
            print(pay)
    else:
        parser.print_help()


if __name__ == '__main__':
    # print(picture)
    main()
