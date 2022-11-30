FROM python:3.7

RUN pip3 install requests tweepy

ADD receive_tweets.py .

EXPOSE 5555

CMD ["python3","-u","./receive_tweets.py"]

#WORKDIR /socket

#COPY requirements.txt requirements.txt

#RUN pip3 install -r requirements.txt

#COPY . .

#CMD ["python3"]

