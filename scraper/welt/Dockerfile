FROM python:3

ADD welt_scraper.py /

RUN pip install beautifulsoup4
RUN pip install requests
RUN pip install pymongo

CMD ["python", "./welt_scraper.py" ]