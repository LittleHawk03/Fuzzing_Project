import argparse
from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from FileInclusion import fileinclusion
from WebConfig import crawler
from prettytable import PrettyTable
from threading import Thread
from Logging import log as Log

picture = Log.R + """
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

def crawler_and_check_sqlI(url, vulnerable_url):
    cr = crawler.Crawler()
    cr.crawl(url, 1)
    cr.visited_link.append(url)
    for url in cr.visited_link:
        scanSqlErrorBase.scan_sql_error_base_in_url(url, vulnerable_url)


def crawler_and_check_xss(url, vulnerable_url):
    cr = crawler.Crawler()
    cr.crawl(url, 1)
    cr.visited_link.append(url)
    for url in cr.visited_link:
        xssFuzz.scan_in_a_url(url, vulnerable_url)


def crawler_and_check_fileI(url, vulnerable_url):
    cr = crawler.Crawler()
    cr.crawl(url, 1)
    cr.visited_link.append(url)
    for url in cr.visited_link:
        fileinclusion.scaner_file_inclusion(url,vulnerable_url)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="target url for scanning", type=str, dest='target')
    parser.add_argument('-c', '--crawler', help="the option for auto crawler from a url", type=int, default=2, dest='crawler')
    parser.add_argument('-s', '--sql', help="auto detect a sql injection from a url", action='store_true', dest='sql')
    parser.add_argument('-x', '--xss', help="auto detect a sxx vulnerable from a url", action='store_true', dest='xss')
    parser.add_argument('-f', '--file', help="auto detect a file inclusion from a url", action='store_true', dest='file')
    parser.add_argument('-a' '--auto', help="auto crawler an scanner all url after crawler url form a website", action='store_true', dest='auto')
    parser.add_argument('-ps', '--payloadsqli', help="show all payload of sql injection", action='store_true', dest='ps')
    parser.add_argument('-px', '--payloadxss', help="show all payload of xss vulnerable", action='store_true', dest='px')
    args = parser.parse_args()
    if args.target is not None and args.sql:
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
    elif args.target is not None and args.xss:
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
    elif args.target is not None and args.file:
        vulnerable_url = []
        t1 = Thread(target=crawler_and_check_fileI, args=(args.target, vulnerable_url,))
        t1.start()
        t1.join()

        table = PrettyTable()
        table.add_rows(vulnerable_url)
        print(table)
    elif args.target is not None and args.crawler:
        cr = crawler.Crawler()
        cr.crawl(args.target, args.crawler)
        cr.visited_link.append(args.target)
        print(cr.visited_link)
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
    print(picture)
    main()
