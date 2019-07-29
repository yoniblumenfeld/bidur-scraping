import grequests
import multiprocessing

class ScrapeRequests:
    def __init__(self,base_search_url,search_keywords_list,processors=multiprocessing.cpu_count()//2):
        self.base_search_url = base_search_url
        self.search_keywords_list = search_keywords_list
        self.processors = processors
        self.reponses = []

    def get(self,url):
        return grequests.get(url).send()

    def __create_requests_pool(self):
        pool = multiprocessing.Pool(processes=self.processors)
        return pool

    def __apply_requests(self):
        pool = self.__create_requests_pool()

        requests_list = [pool.apply_async(self.get,args=(url,)) for url in
                         (self.base_search_url+keyword for keyword in self.search_keywords_list)]
        pool.close()
        pool.join()
        return requests_list

    def get_async_responses(self):
        return self.__apply_requests()

class AsyncResponsesParser:
    @staticmethod
    def get_async_response(response):
        return response.get().response
    @staticmethod
    def get_async_responses(responses_list):
        return [AsyncResponsesParser.get_async_response(response) for response in responses_list]

if __name__ == '__main__':
    url = r'https://www.zappa-club.co.il/AllShows?free='
    scraper = ScrapeRequests(url,['הרצליה','תל אביב'])
    print(AsyncResponsesParser.get_async_responses(scraper.get_async_responses()))