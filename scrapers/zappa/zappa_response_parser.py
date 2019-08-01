from scrapers.generics.generic_response_parser import ResponseParser


class ZappaResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.findAll('a')
        return (parent for parent in all_parents if str(parent.get('href')).find('Show') != -1)

    def get_link(self, parent, base_url):
        return base_url + parent.get('href')

    def get_title(self, parent):
        title = parent.find("div", class_="content_show_title")
        return title.text

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        desc = parent.find("div", class_="content_show_info")
        return desc.findChildren()[1].text

    def get_date(self, parent):
        date = parent.find("div", class_="content_show_datenum")
        return date.text
