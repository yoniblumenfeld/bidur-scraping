import threading
import rabbitmq.settings
from rabbitmq.producers import db_producer
from rabbitmq.workers import db_worker
from rabbitmq import callbacks
from scrapers.barby.barby_scraper import BarbyScraper
from scrapers.cameri.cameri_scraper import CameriScraper
from scrapers.zappa.zappa_scraper import ZappaScraper
import sys


def scrape(scraper):
    scraper.init_scrape_requests()
    data = scraper.get_all_data()
    print(scraper.name, data)
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
    routing_keys = ['barby', 'cameri', 'zappa']
    if len(sys.argv) > 1:
        search_keywords = sys.argv[1:]
        threads = []
    else:
        search_keywords = ['מאור כהן', 'דודו טסה', 'שלמה ארצי', 'הריון', 'עומר אדם', 'יוני בלוך', 'טונה', 'מוניקה סקס',
                           "guy"]
        worker_thread = start_db_insertions_worker([name for name in routing_keys])
        threads = [worker_thread]
        worker_thread.start()
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=', search_keywords)
    barby = BarbyScraper('https://www.barby.co.il/', [])
    cameri = CameriScraper('https://www.cameri.co.il/search.php?f=', search_keywords)
    # tzavta = TzavtaScraper('https://www.tzavta.co.il/Index.aspx?c=0&s=', search_keywords)
    my_scrapers = [cameri, barby, zappa, ]

    for scraper in my_scrapers: threads.insert(0, threading.Thread(target=scrape, args=(scraper,)))

    for thread in threads:
        if not thread.is_alive(): thread.start()
    for thread in threads: thread.join()


if __name__ == '__main__':
    main()
