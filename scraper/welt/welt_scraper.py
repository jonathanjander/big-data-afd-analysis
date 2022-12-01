from bs4 import BeautifulSoup
import requests
import time
import pymongo
from datetime import date, datetime


def filter_titles(titles):
    result = []
    for element in titles:
        if any(x in element for x in filter_criteria()):
            result.append(element)
    return result


def filter_criteria():
    return ["Flüchtling", "Weidel", "Wagenknecht"]


def main():
    client = pymongo.MongoClient("mongodb://localhost:27023/")
    db = client["newspaperdb"]
    titles = db["titles"]
    while True:
        pre_path = "https://www.welt.de/schlagzeilen/nachrichten-vom-"
        ending_path = ".html"
        actual_date = date.today()
        actual_date = actual_date.strftime("%d-%m-%Y")
        url = pre_path + actual_date + ending_path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.getText()[soup.getText().find('Alle Texte von'):]
        text = text.split("|")
        data = []
        for element in text:
            data.append(element[element.find("Ressort:") + 8:-11])
        data = filter_titles(data)
        actual_date = date.today()
        actual_date = actual_date.strftime("%d.%m.%Y")
        existing_titles = []
        for x in titles.find():
            if x.get('date') == actual_date:
                existing_titles.append(x.get('Title'))

        newspaper_titles = []
        for element in data:
            if element not in existing_titles:
                newspaper_titles.append({"date": actual_date, "Title": element})

        if len(newspaper_titles) != 0:
            titles.insert_many(newspaper_titles)

        time.sleep(calculate_sleep_time())


def calculate_sleep_time():
    five_minutes = 300
    twelve_hours = 43200
    if datetime.today().hour == 23 and datetime.today().minute > 50:
        return twelve_hours
    else:
        return five_minutes


if __name__ == '__main__':
    main()
