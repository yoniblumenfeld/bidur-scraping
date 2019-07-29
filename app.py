import webbrowser

from scrapers.zappa.zappa_scraper import ZappaScraper


def open_new_tab(url):
    webbrowser.open(url)

def main():
    zappa = ZappaScraper('https://www.zappa-club.co.il/AllShows?free=',
                          ['דודו טסה'])
    zappa.init_scrape_requests()
    zappa_links = zappa.get_all_links()
    #for key,val in zappa_links.items():
    #    [open_new_tab(res) for res in val]
    print(zappa_links)

if __name__ == '__main__':
    main()