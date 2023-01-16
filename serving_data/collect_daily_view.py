import pymongo
from datetime import datetime

"""
Convert the stored sentiment_probabilities to three floats
"""
def extract_values(string):
    # Extract innermost list from string
    inner_list = string[2:-2]

    # Split inner list into sublists
    sublists = inner_list.split("], [")

    # Extract values from sublists and convert to floats
    values = []
    for sublist in sublists:
        # Split sublist into label and value
        label, value = sublist.split(", ")

        # Remove quotes from label
        label = label[2:-1]

        # Remove quotes and brackets from value
        value = value[1:-2]
        if value[-1] == "-":
            value = 0
        else:
            value = float(value)

        values.append(value)

    # Return values as tuple
    return tuple(values)


# Collectiong all raw data between the first of December till 20th December
def main():
    # Establish a connection to the MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    titles_db = client["Newspaperdb"]
    newspaper_titles = titles_db["Titles"]
    tweet_db = client["Big-Data-DB"]
    tweets = tweet_db["Tweets"]
    # timestamp of the last data collection
    termination_timestamp = 1671476400
    # timestamp of the first of December
    actual_timestamp = 1669849620  # 1669849620
    timestamp_whole_day = 86400

    while True:
        query_titles = {"Timestamp": {"$gte": actual_timestamp, "$lt": actual_timestamp + timestamp_whole_day}}
        titles_cursor = newspaper_titles.find(query_titles)

        keywords = ["Flüchtling", "Weidel", "Wagenknecht", "Ukraine", "AfD", "Putin"]
        found_keywords = []

        for titles in titles_cursor:
            for keyword in keywords:
                if keyword in titles['Title']:
                    found_keywords.append(keyword)

        # View collect all data from a whole day
        view = {}
        dt_object = datetime.fromtimestamp(actual_timestamp)
        actual_date = dt_object.strftime("%d.%m.%Y")
        view["Date"] = actual_date
        view["Timestamp"] = actual_timestamp
        for keyword in found_keywords:
            if keyword not in view:
                view[keyword] = 1
            else:
                view[keyword] += 1

        # collect all tweets of one day and store in the view
        query_tweets = {
            "timestamp": {"$gte": str(actual_timestamp), "$lt": str(actual_timestamp + timestamp_whole_day)}}
        tweets_cursor = tweets.find(query_tweets)
        count_of_tweets = 0
        sentiment = {
            "neutral": 0,
            "positive": 0,
            "negative": 0
        }
        positive_sentiment = 0
        negative_sentiment = 0
        neutral_sentiment = 0
        for tweet in tweets_cursor:
            count_of_tweets += 1
            for key in sentiment.keys():
                if key == tweet["sentiment"][2:-2]:
                    sentiment[key] += 1
            actual_sentiment = (extract_values(tweet["sentiment_probabilities"]))
            positive_sentiment += actual_sentiment[0]
            negative_sentiment += actual_sentiment[1]
            neutral_sentiment += actual_sentiment[2]
        if count_of_tweets != 0:
            positive_sentiment = positive_sentiment / count_of_tweets
            negative_sentiment = negative_sentiment / count_of_tweets
            neutral_sentiment = neutral_sentiment / count_of_tweets
            view["Avg_positive"] = positive_sentiment
            view["Avg_negative"] = negative_sentiment
            view["Avg_neutral"] = neutral_sentiment
            view["Absolut_positive"] = sentiment["positive"]
            view["Absolut_negative"] = sentiment["neutral"]
            view["Absolut_neutral"] = sentiment["negative"]
            view["Tweet_count"] = count_of_tweets
        actual_timestamp = actual_timestamp + timestamp_whole_day
        if actual_timestamp + timestamp_whole_day > termination_timestamp:
            break
        view_of_one_day = [view]
        view_db = client["TestView"]
        view_collection = view_db["View"]
        view_collection.insert_many(view_of_one_day)


if __name__ == '__main__':
    main()
