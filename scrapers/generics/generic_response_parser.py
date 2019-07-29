from abc import abstractmethod, ABC
from bs4 import BeautifulSoup as bs
import json


class ResponseParser(ABC):
    def __init__(self, response, base_url):
        self.response = response
        self.soup = bs(response.text, 'html.parser')
        self.base_url = base_url

    def get_data(self):
        """
        Method used to compose and return json object containing
        relevant data
        """
        responses = []
        for parent in self.get_parents():
            responses.append(
                {
                    'link': self.get_link(parent,self.base_url),
                    'title': self.get_title(parent),
                    'description': self.get_description(parent),
                    'date': self.get_date(parent)

                }
            )
        # TODO:rethink dumping to json on return
        return responses



    @abstractmethod
    def get_parents(self):
        pass

    @abstractmethod
    def get_date(self, parent):
        pass

    @abstractmethod
    def get_link(self, parent, base_url):
        """
        Method used to parse response with BeautifulSoup
        returns the complete urls for each of the results found.
        """
        pass

    @abstractmethod
    def get_title(self, parent):
        """
        Method used to parse response with BeautifulSoup
        returns the title for each of the results found.
        """
        pass

    @abstractmethod
    def get_date(self, parent):
        """
        Method used to parse response with BeautifulSoup
        returns the date for each of the results found.
        """
        pass

    @abstractmethod
    def get_img(self, parent):
        """
        Method used to parse response with BeautifulSoup
        returns the img for each of the results found.
        """
        pass

    @abstractmethod
    def get_description(self, parent):
        """
        Method used to parse response with BeautifulSoup
        returns the description for each of the results found.
        """
        pass
