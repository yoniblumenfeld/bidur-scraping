from scrapers.tzavta_scraper import TzavtaScraper

def main():
    tzavta = TzavtaScraper('https://www.zappa-club.co.il/AllShows?free=',
                           ['הרצליה','תל אביב','ירושלים'])
    tzavta.init_scrape_requests()
    tzavta_links = tzavta.get_all_links()
    print(tzavta_links)

if __name__ == '__main__':
    main()