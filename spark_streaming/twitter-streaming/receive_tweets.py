import tweepy
import socket
# from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_TOKEN, BEARER
from datetime import datetime
from germansentiment import SentimentModel

BEARER = 'AAAAAAAAAAAAAAAAAAAAAOtkigEAAAAAliy%2B7td2nmGkVVCj7orrLwhjJ8w%3DpM4IvekgfVzgAs7NnJoXgLrW1q67jpc2VRjeSmqJCCj8cLpfoc'


class TwitterV2Stream(tweepy.StreamingClient):
    def __init__(self, csocket, b_token):
        self.client_socket = csocket
        tweepy.StreamingClient.__init__(self=self, bearer_token=b_token)

    def on_connect(self):
        print("connected")

    def on_tweet(self, tweet):
        try:
            if isinstance(tweet.text, str) and tweet.referenced_tweets == None:
                # tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S")
                output = str(tweet.text)
                if tweet.created_at is not None:
                    output = output + str(";") + str(tweet.created_at)
                else:
                    ts = datetime.timestamp(datetime.now())
                    output = output + str(";") + str(ts)
                sentiment = get_sentiment(tweet.text)
                output = output + str(';' + sentiment[0] + ';' + sentiment[1] + '\n')
                print(output)
                print("-")
                print("-")
                self.client_socket.send(output.encode('utf-8'))
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            print("-")
            print("-")
        return True


def send_tweets_v2(c_socket):
    twitter_client = TwitterV2Stream(csocket=c_socket, b_token=BEARER)
    # "#noafd" -lang:de didnt work aka didnt filter for language
    twitter_client.add_rules(
        [tweepy.StreamRule('#afd lang:de'), tweepy.StreamRule('#noafd lang:de'), tweepy.StreamRule('afd lang:de')])
    # twitter_client.delete_rules(['1592908834301001729','1592908834301001730','1592915146938224646','1592919964968681472','1592919964968681473','1592919964968681474'])
    print(twitter_client.get_rules())
    twitter_client.filter(tweet_fields=['referenced_tweets'])


def get_sentiment(tweet):
    model = SentimentModel()
    classes, probabilities = model.predict_sentiment([tweet], output_probabilities=True)
    return [str(classes), str(probabilities)]


if __name__ == "__main__":
    new_skt = socket.socket()  # initiate a socket object
    # host = "127.0.0.1"  # local machine address
    host = "0.0.0.0"  # local machine address
    port = 5555  # specific port for your service.
    new_skt.bind((host, port))  # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)  # waiting for client connection.
    c, addr = new_skt.accept()  # Establish connection with client. it returns first a socket object, c and the address bound to the socket

    print("Received request from: " + str(addr))
    # and after accepting the connection, we will send the tweets through the socket
    send_tweets_v2(c)
