import argparse
import threading

from SQLi import scanSqlErrorBase
from XSS import xssFuzz
from FileInclusion import fileinclusion
from WebConfig import crawler, crawler2
from prettytable import PrettyTable
from threading import Thread
from urllib.parse import urlparse
from Logging import log as Log
import time


banner_text = Log.G + '''
     ▀█████▄    ,████▌
      ╙██████µ  █████ ███████╗██╗   ██╗███████╗███████╗██╗███╗   ██╗ ██████╗  
         ▀████▄ ████  ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██║████╗  ██║██╔════╝ 
          ,▄▄█████▀   █████╗  ██║   ██║  ███╔╝   ███╔╝ ██║██╔██╗ ██║██║  ███╗
        ▄█▀████████C  ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██║██║╚██╗██║██║   ██║
    ░  █████████████` ██║     ╚██████╔╝███████╗███████╗██║██║ ╚████║╚██████╔╝
      ░█████████████░ ██║     ╚██████╔╝███████╗███████╗██║██║ ╚████║╚██████╔╝
         ▀▀████████▀, ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
         ▄,██▌▀▀▀▄▄ ▀        <<<<<<<< STARTING FUZZ >>>>>>>>       
         ▐▀▀▀▌▀``
    ''' + ']'

## hàm gọi đê thực hiện cào url sử dụng thread
def crawler_url(url, level=1):
    cr = crawler2.Crawler()
    cr.crawl(url, level)
    cr.visited_link.append(url)
    return cr.visited_link


def fuzzable_list(crawler_list):
    fuzzable = []
    for url in crawler_list:
        queries = urlparse(url).query
        if queries != '':
            list_query = []
            for query in queries.split("&"):
                list_query.append(query[0:query.find("=") + 1])
            query = "&".join([param for param in list_query])
            final_url = url.replace(queries,query)
            if final_url not in fuzzable:
                fuzzable.append(final_url)
        else:
            fuzzable.append(url)
    return fuzzable

## hàm để kiểm tra sql injection
def crawler_and_check_sqlI(urls, vulnerable_url, crawler_list):
    threads = []
    for url in crawler_list:
        t = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_url, args=(url, vulnerable_url,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        # t.join()


## hàm để kiểm tra xss sử dụng thread
def crawler_and_check_xss(urls, vulnerable_url,crawler_list):
    threads = []
    # cr = crawler_url(url, level=level)
    for url in crawler_list:
        t = Thread(target=xssFuzz.scan_form_in_url, args=(url, vulnerable_url))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


# hàm kiểm tra file inclusion sử dụng thread
def crawler_and_check_fileI(urls, vulnerable_url, crawler_list):
    threads = []
    # cr = crawler_url(url)
    for url in crawler_list:
        t = Thread(target=fileinclusion.scaner_file_inclusion, args=(url, vulnerable_url))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


""""
    ừm để có thể quét tất cả một trang web thì công việc đó sẽ như sau crawler -> check sql injection -> check xss -> check file
    để thực hiện tuần tự thì nó rất là lâu, lâu cực, lâu điên đảo luôn ấy nên mình sử dụng phương pháp lập trình đa luồng
     for url in cr:
        t = Thread(target=fileinclusion.scaner_file_inclusion, args=(url, vulnerable_url))
        t.start()

    for thread in threads:
        thread.join()
        
    hiểu đơn giản thì mình sẽ chạy các chức năng này một các song song mà không phải tuần tự.
    
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="target url for scanning", type=str, dest='target')
    parser.add_argument('-c', '--crawler', help="the option for auto crawler from a url", action='store_true', dest='crawler')
    parser.add_argument('-s', '--sql', help="auto detect a sql injection from a url", action='store_true', dest='sql')
    parser.add_argument('-x', '--xss', help="auto detect a sxx vulnerable from a url", action='store_true', dest='xss')
    parser.add_argument('-f', '--file', help="auto detect a file inclusion from a url", action='store_true',
                        dest='file')
    parser.add_argument('-a', '--auto', help="auto crawler an scanner all url after crawler url form a website",
                        action='store_true', dest='auto')
    parser.add_argument('-ps', '--payloadsqli', help="show all payload of sql injection", action='store_true',
                        dest='ps')
    parser.add_argument('-px', '--payloadxss', help="show all payload of xss vulnerable", action='store_true',
                        dest='px')
    args = parser.parse_args()
    if args.target is not None and args.sql:
        t = time.time()
        vulnerable_url = []
        Log.info("start Crawling ... ")
        crawler_list = crawler_url(args.target, level=1)
        fuzzable_url = fuzzable_list(crawler_list)
        t1 = Thread(target=crawler_and_check_sqlI, args=(args.target, vulnerable_url, fuzzable_url,))
        t2 = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_form, args=(args.target, vulnerable_url))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


        table = PrettyTable(['url','type url','type vul','payload'])
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.xss:
        t = time.time()
        vulnerable_url = []

        Log.info("start Crawling ... ")
        crawler_list = crawler_url(args.target,level=1)
        t1 = Thread(target=crawler_and_check_xss, args=(args.target, vulnerable_url, crawler_list, ))
        t2 = Thread(target=xssFuzz.scan_in_a_url, args=(args.target, vulnerable_url,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        table = PrettyTable(['url','type url','type vul','payload'])
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.file:
        t = time.time()
        vulnerable_url = []
        Log.info("start Crawling ... ")
        crawler_list = crawler_url(args.target, level=1)
        t1 = Thread(target=crawler_and_check_fileI, args=(args.target, vulnerable_url,crawler_list,))
        t1.start()
        t1.join()


        table = PrettyTable(['url','type url','type vul','payload'])
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.auto:
        t = time.time()
        vulnerable_url = []
        Log.info("start Crawling ... ")
        cr = crawler_url(args.target,1)

        t1 = Thread(target=crawler_and_check_sqlI, args=(args.target, vulnerable_url, cr,))
        t2 = Thread(target=scanSqlErrorBase.scan_sql_error_base_in_form, args=(args.target, vulnerable_url))
        t3 = Thread(target=crawler_and_check_xss, args=(args.target, vulnerable_url,cr ,))
        t4 = Thread(target=xssFuzz.scan_form_in_url, args=(args.target, vulnerable_url,))
        t5 = Thread(target=crawler_and_check_fileI, args=(args.target, vulnerable_url, cr,))
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

        table = PrettyTable(['url','type url','type vul','payload'])
        Log.info('vul number : ' + str(len(vulnerable_url)))
        table.add_rows(vulnerable_url)
        print(table)
        Log.info('time : ' + str(time.time() - t))
    elif args.target is not None and args.crawler:
        t = time.time()
        # tạo đối tương crawler rồi tiến hành crawler
        # url = args.target, level = args.crawler được lấy từ terminal
        cr = crawler2.Crawler()
        level = int(input('cawler level  = '))
        Log.info("start Crawling ... ")
        cr.crawl(args.target,level)
        cr.visited_link.append(args.target)
        #tạo bảng rồi thêm cột bao gồm các cột là các url vừa crawler được
        table = PrettyTable()
        table.add_column('URL',cr.visited_link)
        print(table)
        Log.info('crawler success with ' + str(len(cr.visited_link)) + ' url is found')
        Log.info('time : ' + str(time.time() - t))
    elif args.ps:
        f = open("SQLi/sql.txt", "r")
        for pay in f.readlines():
            print(pay)
    elif args.px:
        f = open("XSS/xss.txt", "r")
        for pay in f.readlines():
            print(pay)
    elif args.target is not None:
        parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    print(banner_text)
    main()
