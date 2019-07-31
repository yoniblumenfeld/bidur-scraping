from scrapers.generics.generic_response_parser import ResponseParser


class TzavtaResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.find('ul', class_="event-list").findAll('li')
        return (parent for parent in all_parents)

    def get_link(self, parent, base_url):
        link = parent.find('a').get('href')
        return base_url + link[link.find('?')+1:]

    def get_title(self, parent):
        #TODO: still wont work :(
        title = parent.find('div', class_="caption").find('h2').text
        return title

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        pass

    def get_date(self, parent):
        date = parent.find('div', class_="date")
        return date.text
