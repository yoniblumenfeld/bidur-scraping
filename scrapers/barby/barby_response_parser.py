from scrapers.generics.generic_response_parser import ResponseParser


class BarbyResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.findAll('table', class_="tbl_cat")
        return (p for p in all_parents)

    def get_link(self, parent, base_url):
        link = parent.find('td', class_="defaultRowHeight").find('div', class_="defShowListMain").find('a').get('href')
        return base_url + link

    def get_title(self, parent):
        pass

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        pass

    def get_date(self, parent):
        pass
