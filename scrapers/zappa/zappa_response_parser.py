from scrapers.generics.generic_response_parser import ResponseParser

class ZappaResponseParser(ResponseParser):
    def __init__(self,response,base_url):
        super(ZappaResponseParser).__init__(response, base_url)

    def get_link(self, base_url):
        pass

    def get_title(self):
        pass

    def get_img(self):
        pass

    def get_description(self):
        pass

    def get_data(self):
        pass

