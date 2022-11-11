from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import os
import sys
from textblob_de import TextBlobDE
from germansentiment import SentimentModel


def preprocessing(tweets_pre):

    tweets_pre = tweets_pre.withColumn('value', F.regexp_replace('value', r'http\S+', ''))
    tweets_pre = tweets_pre.withColumn('value', F.regexp_replace('value', '@\w+', ''))
    tweets_pre = tweets_pre.withColumn('value', F.regexp_replace('value', 'RT:', ''))
    tweets_pre = tweets_pre.na.replace('', None)
    tweets_pre = tweets_pre.na.drop()
    return tweets_pre


def sentiment(tweets):
    sentiment_detection_udf = udf(sentiment_detection, StringType())
    tweets = tweets.withColumn("sentiment", sentiment_detection_udf('value'))
    return tweets


def sentiment_detection(text):
    return TextBlobDE(text).sentiment.polarity
    # way too computationally expensive, we should do the sentiment calculation at a later state
    # text_arr = [text]
    # model = SentimentModel()
    # return model.predict_sentiment(text_arr)


def tutorial_example_for_testing(lines):
    lines.printSchema()
    words = lines.select(
        explode(
            split(lines.value, " ")
        ).alias("word")
    )
    # Generate running word count
    word_counts = words.groupBy("word").count()
    return word_counts


if __name__ == "__main__":
    # fixing a bug with this
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    # create Spark session
    spark = SparkSession.builder.appName("AfDTweetAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "127.0.0.1").option("port", 5555).option("encoding", 'utf-8').load()
    tweets = preprocessing(lines)
    tweets = sentiment(tweets)
    tweets.printSchema()
    tweets = tweets.repartition(1)
    # encoding still doesn't work
    query = tweets.writeStream.queryName("all_tweets") \
        .outputMode("append").format("parquet") \
        .option("path", "./parquet_files") \
        .option("checkpointLocation", "./check") \
        .option("encoding", 'utf-8') \
        .trigger(processingTime='60 seconds') \
        .start()

    """
    # just for testing over the console
    wordcounts = tutorial_example_for_testing(lines)
        # Start running the query that prints the running counts to the console
        query = wordcounts \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .start()
    """
    query.awaitTermination()
