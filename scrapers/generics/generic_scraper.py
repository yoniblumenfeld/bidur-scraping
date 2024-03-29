from abc import abstractmethod, ABC
import urllib.parse


class GenericBidurScraper(ABC):
    """
    Abstract class for the creation of scrapers for
    the BidurScraping project.
    this is the skeleton of every scraper.
    """

    def __init__(self, search_url, search_keywords_list, name):
        self.search_url = search_url
        self.name = name
        self.search_keywords_list = search_keywords_list
        splitted_search = self.search_url.split('/') #TODO://might need to find more generic way, could be buggy
        self.base_url = '{}//{}'.format(splitted_search[0],splitted_search[2])
        self.ready_responses = None
        super().__init__()

    @abstractmethod
    def get_all_data(self):
        """
        Abstract method used to get all the links that are relevant
        to the search keywords set.
        Using the responses returned from the MPTasks class after calling
        the init_scrape_requests on thia class - uses the self.ready_responses iterable.
        Using BeautifulSoup to parse the returned html files.
        """
        pass

    @abstractmethod
    def add_search_keyword(self, keyword):
        """
        Abstract method used to add search_keyword to the search_keywords_list
        used to scrape relevant resource.
        """
        pass

    @abstractmethod
    def reset_search_keywords_and_set(self, keywords):
        """
        Abstract method used to reset the self.search_keywords_list,
        and resetting to the new keywords passed to this function.
        """
        pass

    @abstractmethod
    def init_scrape_requests(self):
        """
        Abstract method used to initiate the proper scrape requests
        using the MPTasks module.
        requests should be made using grequests (async http requests).
        the MPTasks module should return the ready requests.
        the ready requests should be added to self.ready_responses list.
        """
        pass

    @abstractmethod
    def parse_response(self,response):
        """
        Abstract method used to parse each response text in order to extract
        viable data
        """
        pass

    def set_search_url(self, new_search_url):
        """
        Method used to edit the search url.
        Usually wont do much except for setting the self.search_url variable.
        Might be used when extra logic is needed before setting the new search url.
        """
        self.search_url = new_search_url

    def decode_js_url(self, string):
        return urllib.parse.unquote(string)
