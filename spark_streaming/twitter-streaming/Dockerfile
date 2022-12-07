# Get the latest base image for python
FROM python:3.7

RUN pip3 install germansentiment
RUN pip3 install tweepy
# Put files at the image '/socket-host/' folder.
ADD receive_tweets.py /socket-host/
# '/socket-host/' is base directory
WORKDIR /socket-host/
# Expose port 5555 in the container
EXPOSE 5555
# execute the command
CMD [ "python3", "receive_tweets.py" ]