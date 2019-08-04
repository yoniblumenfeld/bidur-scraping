from bs4 import BeautifulSoup as bs
from scrapers.generics.generic_scraper import GenericBidurScraper
from scrapers.multiprocessing_models.scrape_requests import AsyncResponsesParser, ScrapeRequests
from scrapers.zappa.zappa_response_parser import ZappaResponseParser


class ZappaScraper(GenericBidurScraper):
    def __init__(self, search_url, search_keywords_list=None):
        super().__init__(search_url, search_keywords_list if search_keywords_list else [''], 'zappa')
        self.ready_responses = []

    def add_search_keyword(self, keyword):
        self.search_keywords_list.append(keyword)

    def reset_search_keywords_and_set(self, keywords):
        self.search_keywords_list = [keywords]

    def get_all_data(self):
        return self.ready_responses

    def parse_response(self,response):
        parser = ZappaResponseParser(response,self.base_url)
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
            res = self.parse_response(response)
            for obj in res:
                obj['keyword'] = self.decode_js_url(response.url.replace(self.search_url,''))
            self.ready_responses.append(res)

