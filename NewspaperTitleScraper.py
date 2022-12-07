from bs4 import BeautifulSoup
import requests
import threading
from datetime import date
import json


def filter_titles(titles):
    result = []
    for element in titles:
        if any(x in element for x in filter_criteria()):
            result.append(element)
    return result


def filter_criteria():
    return ["Flüchtling", "Ukraine", "Weidel", "Wagenknecht"]


class NewspaperTitleScraper(threading.Thread):
    def __init__(self, thread_name):
        super().__init__()
        self.name = thread_name
        self.interrupted = False
        settings_path = "../settings/" + thread_name + ".json"
        with open(settings_path, 'r', encoding='utf-8') as f:
            my_data = json.load(f)
        self.pre_path = my_data["pre_path"]
        self.ending_path = my_data["ending_path"]
        self.date_format = my_data["date_format"]

    def run(self):
        # TODO -> date after 00:00 http request receive 404
        # actual_date = date.today()
        # actual_date = actual_date.strftime(self.date_format)
        actual_date_bild = '2022/11/19'
        actual_date_welt = '19-11-2022'
        data = self.receive_titles_from_date(actual_date_welt)
        data = filter_titles(data)
        for element in data:
            print(element)

    def interrupt(self):
        self.interrupted = True

    def receive_titles_from_date(self, actual_date):
        url = self.pre_path + actual_date + self.ending_path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        if self.name == "Bild":
            return self.find_table_titles_bild(soup)
        elif self.name == "Welt":
            table = self.find_table_titles_welt(soup)

    @staticmethod
    def find_table_titles_bild(soup):
        table = soup.find("div", attrs={"class": "txt"})
        data = []
        for element in table.contents[3]:
            data.append(element.text[12:])
        return data

    @staticmethod
    def find_table_titles_welt(soup):
        # soup.find("div", attrs={"class": "c-teaser__headline-link is-teaser-link"})
        text = soup.getText()[soup.getText().find('Alle Texte von'):]
        text = text.split("|")
        #text = text[text.find(":")]
        for element in text:
            print(element[element.find("Ressort:")+8:])
            #TODO Cut Datum
        return True
