import webbrowser

from scrapers.zappa.zappa_scraper import ZappaScraper
from scrapers.tzavta.tzavta_scraper import TzavtaScraper


def open_new_tab(url):
    webbrowser.open(url)


def get_data(scraper):
    scraper.init_scrape_requests()
    return scraper.get_all_data()


def main():
    search_keywords = ['מאור כהן', 'דודו טסה', 'שלמה ארצי']
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=', search_keywords)

    tzavta = TzavtaScraper('https://www.tzavta.co.il/Index.aspx?c=0&s=', search_keywords)
    my_scrapers = [zappa, tzavta]
    for scraper in my_scrapers:
        print(get_data(scraper))


if __name__ == '__main__':
    main()
