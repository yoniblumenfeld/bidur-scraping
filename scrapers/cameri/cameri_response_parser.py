from scrapers.generics.generic_response_parser import ResponseParser


class CameriResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.find('div', class_="search-results-content").find('div', class_="item")
        return (parent for parent in all_parents)

    def get_link(self, parent, base_url):
        link = parent.find('div', class_="wrap").find('h3', class_="title").find('a').get('href')
        print(parent)
        return link

    def get_title(self, parent):
        title = parent.find('div', class_="wrap").find('h3', class_="title").find('a')
        return title.text

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        pass

    def get_date(self, parent):
        pass
