import threading
import webbrowser

import rabbitmq.settings
from bidurdb import db
from rabbitmq.producers import db_producer
from rabbitmq.workers import db_worker
from scrapers.barby.barby_scraper import BarbyScraper
from scrapers.cameri.cameri_scraper import CameriScraper
from scrapers.zappa.zappa_scraper import ZappaScraper
from rabbitmq import callbacks


def open_new_tab(url):
    webbrowser.open(url)


def get_data(scraper):
    scraper.init_scrape_requests()
    data = scraper.get_all_data()
    producer = db_producer.DbProducer(exchange_type=rabbitmq.settings.DB_INSERTIONS_EXCHANGE_TYPE,
                                      exchange_name=rabbitmq.settings.DB_INSERTIONS_EXCHANGE_NAME,
                                      routing_key=scraper.name)
    producer.publish(data)
    producer.close()


def start_db_insertions_worker(routing_keys=[], exchange_type=rabbitmq.settings.DB_INSERTIONS_EXCHANGE_TYPE,
                               exchange_name=rabbitmq.settings.DB_INSERTIONS_EXCHANGE_NAME):
    worker = db_worker.DbWorker(exchange_type=exchange_type,
                                exchange_name=exchange_name,
                                routing_keys=routing_keys,
                                callback=callbacks.db_insert_callback)
    worker_thread = threading.Thread(target=worker.consume)
    return worker_thread

def main():
    search_keywords = ['מאור כהן', 'דודו טסה', 'שלמה ארצי', 'הריון', 'עומר אדם', 'יוני בלוך', 'טונה', 'מוניקה סקס']
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=', search_keywords)
    barby = BarbyScraper('https://www.barby.co.il/', [])
    cameri = CameriScraper('https://www.cameri.co.il/search.php?f=', search_keywords)
    # tzavta = TzavtaScraper('https://www.tzavta.co.il/Index.aspx?c=0&s=', search_keywords)

    my_scrapers = [cameri, barby, zappa, ]  # tzavta]
    worker_thread = start_db_insertions_worker([scraper.name for scraper in my_scrapers])
    worker_thread.start()
    threads = []

    for scraper in my_scrapers:
        threads.append(threading.Thread(target=get_data, args=(scraper,)))
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    worker_thread.join()
    print(db.find_results_by_keyword('טונה'))


if __name__ == '__main__':
    main()
