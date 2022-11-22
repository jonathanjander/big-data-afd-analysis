from bs4 import BeautifulSoup
import requests
import time


def filter_titles(titles):
    result = []
    for element in titles:
        if any(x in element for x in filter_criteria()):
            result.append(element)
    return result


def filter_criteria():
    return ["Flüchtling", "Ukraine", "Weidel", "Wagenknecht"]


def main():
    for i in range(0, 5):
        pre_path = "https://www.bild.de/archive/"
        ending_path = "/index.html"
        actual_date = '2022/11/19'
        url = pre_path + actual_date + ending_path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("div", attrs={"class": "txt"})
        data = []
        for element in table.contents[3]:
            data.append(element.text[12:])
        data = filter_titles(data)

        for element in data:
            print(element)
        print("____DAY END start Sleep 30 sec")
        time.sleep(30)


if __name__ == '__main__':
    main()
