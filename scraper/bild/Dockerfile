FROM python:3

ADD bild_scraper.py /

RUN pip install beautifulsoup4
RUN pip install requests
RUN pip install pymongo

CMD ["python", "./bild_scraper.py" ]