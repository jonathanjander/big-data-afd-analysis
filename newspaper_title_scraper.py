from bs4 import BeautifulSoup
import requests

def scrape_newspaper_title():
    url = f"https://www.bild.de/archive/2022/10/1/index.html "
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", attrs={"class": "txt"})
    data = []
    for element in table.contents[3]:
        data.append(element.text[12:])
    return data


