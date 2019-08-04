from scrapers.generics.generic_scraper import GenericBidurScraper
from scrapers.multiprocessing_models.scrape_requests import AsyncResponsesParser, ScrapeRequests
from scrapers.barby.barby_response_parser import BarbyResponseParser


class BarbyScraper(GenericBidurScraper):
    def __init__(self, search_url, search_keywords_list=None):
        super().__init__(search_url, search_keywords_list if search_keywords_list else [''], 'Barby')
        self.ready_responses = {}
        self.base_url = 'https://www.barby.co.il/'

    def add_search_keyword(self, keyword):
        self.search_keywords_list.append(keyword)

    def reset_search_keywords_and_set(self, keywords):
        self.search_keywords_list = [keywords]

    def get_all_data(self):
        return self.ready_responses

    def parse_response(self, response):
        parser = BarbyResponseParser(response, self.base_url)
        return parser.get_data()

    """def parse_response(self, response):
        soup = bs(response.text, 'html.parser')
        all_links = soup.findAll('a')
        links = []
        for link in all_links:
            href = link.get('href')
            if str(href).find('Show') != -1:
                links.append(self.base_url+href)
        return links
    """

    def init_scrape_requests(self):
        scrapers = ScrapeRequests(self.search_url, self.search_keywords_list)
        responses = AsyncResponsesParser.get_async_responses(scrapers.get_async_responses())
        for response in responses:
            self.ready_responses[response.url] = self.parse_response(response)
