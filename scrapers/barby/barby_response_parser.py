from scrapers.generics.generic_response_parser import ResponseParser


class BarbyResponseParser(ResponseParser):
    def __init__(self, response, base_url):
        super().__init__(response, base_url)

    def get_parents(self):
        all_parents = self.soup.findAll('td', class_="defaultRowHeight")
        return (parent for parent in all_parents)

    def get_link(self, parent, base_url):
        link = parent.find('div', class_="defShowListMain").find('a').get('href')
        return base_url + link

    def get_title(self, parent):
        title = parent.find('div', class_="defShowListDescHeight").find('div', class_="defShowListDescDiv").text
        return title.strip().replace(r'\n', '')

    def get_img(self, parent):
        pass

    def get_description(self, parent):
        description = parent.find('div', class_='descshortc')
        txt = list(description.text)
        txt.reverse()
        txt = txt[txt.index(" ")+4:]
        txt.reverse()
        return "".join(txt)



    def get_date(self, parent):
        date = parent.find('div', class_='def_titel2A').text
        return date
