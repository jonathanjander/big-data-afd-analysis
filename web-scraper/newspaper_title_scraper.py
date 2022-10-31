from bs4 import BeautifulSoup
import requests


def main():
    url = f"https://www.bild.de/archive/2022/10/1/index.html "
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", attrs={"class": "txt"})
    for element in table.contents[3]:
        print(element.text[12:])


if __name__ == '__main__':
    main()
