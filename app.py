import webbrowser

from scrapers.zappa.zappa_scraper import ZappaScraper
from scrapers.tzavta.tzavta_scraper import TzavtaScraper
from scrapers.barby.barby_scraper import BarbyScraper
from scrapers.cameri.cameri_scraper import CameriScraper


def open_new_tab(url):
    webbrowser.open(url)


def get_data(scraper):
    scraper.init_scrape_requests()
    return scraper.get_all_data()


def main():
    search_keywords = ['מאור כהן', 'דודו טסה', 'שלמה ארצי', 'הריון']
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=', search_keywords)
    barby = BarbyScraper('https://www.barby.co.il/', [])
    cameri = CameriScraper('https://www.cameri.co.il/search.php?f=', search_keywords)
    tzavta = TzavtaScraper('https://www.tzavta.co.il/Index.aspx?c=0&s=', search_keywords)
    my_scrapers = [cameri, barby, zappa, tzavta]
    for scraper in my_scrapers:
        print(get_data(scraper))


if __name__ == '__main__':
    main()
