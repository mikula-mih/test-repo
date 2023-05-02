import threading
import queue
import csv
from concurrent.futures import ThreadPoolExecutor
from web_crawler import *
from CheckableQueue import *

THREAD_COUNT = 20
linksToCrawl = CheckableQueue()

def createCrawlers():
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=run)
        t.daemon = True
        t.start()

def run():
    try:
        Crawler.crawl(threading.current_thread(), url, linksToCrawl)
    except:
        print("Exception thrown with link: {}".format(url))
    linksToCrawl.task_done()


def appendToCSV(result):
    print("Appending result to CSV File: {}".format(result))
    with open('results.csv', 'a') as csvfile:
        resultwriter = csv.writer(
            csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL
        )
        resultwriter.writerow(result)


def main():
    url = input("Website > ")
    Crawler(url)
    linksToCrawl.put(url)
    while not linksToCrawl.empty():
        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            url = linksToCrawl.get()
            futures = []
            if url is not None:
                future = executor.submit(run, url)
                futures.append(future)

            for future in as_completed(futures):
                try:
                    if future.result() != None:
                        appendToCSV(future.result())
                except:
                    print(future.exception())

    print("Total Links Crawled: {}".format(len(Crawler.crawledLinks)))
    print("Total Errors: {}".format(len(Crawler.errorLinks)))

if __name__ == '__main__':
    main()
