from scrapers.generics.generic_response_parser import ResponseParser


class TzavtaResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.findAll('a')
        return (parent for parent in all_parents if str(parent.get('href')).find('EventPage') != -1\
                and str(parent.get("class")) != "['button']")

    def get_link(self, parent, base_url):
        link = parent.get('href')
        return base_url + link[link.find('?')+1:]

    def get_title(self, parent):
        #TODO: still wont work :(
        div = self.soup.find("div", class_="caption")
        for title in div.findAll('h2'):
            return title.text

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        pass

    def get_date(self, parent):
        pass
