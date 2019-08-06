import webbrowser

from bidurdb import db
from scrapers.zappa.zappa_scraper import ZappaScraper
from scrapers.tzavta.tzavta_scraper import TzavtaScraper
from scrapers.barby.barby_scraper import BarbyScraper
from scrapers.cameri.cameri_scraper import CameriScraper
import threading

def open_new_tab(url):
    webbrowser.open(url)


def get_data(scraper):
    scraper.init_scrape_requests()
    data = scraper.get_all_data()
    db.insert_scrape_results(data)
    return data


def main():
    search_keywords = ['מאור כהן', 'דודו טסה', 'שלמה ארצי', 'הריון','עומר אדם','יוני בלוך','טונה','מוניקה סקס']
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=', search_keywords)
    barby = BarbyScraper('https://www.barby.co.il/', [])
    cameri = CameriScraper('https://www.cameri.co.il/search.php?f=',search_keywords)
    tzavta = TzavtaScraper('https://www.tzavta.co.il/Index.aspx?c=0&s=', search_keywords)
    my_scrapers = [cameri, barby, zappa,tzavta]
    threads = []
    for scraper in my_scrapers:
        threads.append(threading.Thread(target=get_data,args=(scraper,)))
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    print(db.find_results_by_keyword('טונה'))


if __name__ == '__main__':
    main()
