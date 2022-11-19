import threading

from bs4 import BeautifulSoup
import requests
import threading
from datetime import date


def receive_titles_from_date(actual_date):
    pre_path = "https://www.bild.de/archive/"
    ending_path = "/index.html"
    url = pre_path + actual_date + ending_path
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", attrs={"class": "txt"})
    data = []
    for element in table.contents[3]:
        data.append(element.text[12:])
    return data


class NewspaperTitleScraper(threading.Thread):
    def __init__(self, thread_name):
        super().__init__()
        self.name = thread_name
        self.interrupted = False

    def run(self):
        actual_date = date.today()
        actual_date = actual_date.strftime("%Y/%m/%d")
        data = receive_titles_from_date(actual_date)
        for element in data:
            print(element)

    def interrupt(self):
        self.interrupted = True
