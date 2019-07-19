from scrapers.generic_scraper import GenericBidurScraper
from bs4 import BeautifulSoup as bs
import grequests


class TzavtaScraper(GenericBidurScraper):
    def __init__(self, search_url, search_keywords_list=None):
        super().__init__(search_url, search_keywords_list if search_keywords_list else [''], 'Tzavta')

    def set_search_url(self, new_search_url):
        super().set_search_url(new_search_url)

    def add_search_keyword(self, keyword):
        self.search_keywords_list.append(keyword)

    def reset_search_keywords_and_set(self, keywords):
        self.search_keywords_list = [keywords]

    def get_all_links(self):
        pass

    def init_scrape_requests(self):
        pass
