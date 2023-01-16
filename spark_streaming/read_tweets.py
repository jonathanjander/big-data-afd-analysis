from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import from_unixtime, to_timestamp
from pyspark.sql.types import *
import socket
from germansentiment import SentimentModel
import os
import sys

def preprocessing(tweets_pre):
    # splits input string into tweets and timestamps (semicolon seperated)
    tweets_pre = tweets_pre.withColumn('tmp', split(col("value"), ';')).withColumn('tweet', col('tmp')[0]).withColumn(
        'timestamp_tweet', col('tmp')[1]).withColumn('sentiment', col('tmp')[2]).withColumn('positive_sentiment_value',col('tmp')[3]).withColumn('negative_sentiment_value',col('tmp')[4]).withColumn('neutral_sentiment_value',col('tmp')[5]).drop('tmp','value')
    # filters tweets
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', r'http\S+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', '@\w+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', 'RT:', ''))
    tweets_pre = tweets_pre.withColumn('formatted_timestamp', to_timestamp(from_unixtime(col('timestamp_tweet'))))
    tweets_pre = tweets_pre.withColumn('positive_sentiment_value', col('positive_sentiment_value').cast(DoubleType()))
    tweets_pre = tweets_pre.withColumn('negative_sentiment_value', col('negative_sentiment_value').cast(DoubleType()))
    tweets_pre = tweets_pre.withColumn('neutral_sentiment_value', col('neutral_sentiment_value').cast(DoubleType()))
    tweets_pre = tweets_pre.na.replace('', None)
    tweets_pre = tweets_pre.na.drop()
    return tweets_pre

def aggregation(tweets):
    tweets_aggregated = tweets.withWatermark("formatted_timestamp", "15 minutes").groupBy("sentiment",
                                                                                         window("formatted_timestamp", "15 minutes")).agg(count("*").alias("sentiment_count"),
                                                                                                                  avg("positive_sentiment_value").alias("avg_positive"),
                                                                                                                  avg("negative_sentiment_value").alias("avg_negative"),
                                                                                                                  avg("neutral_sentiment_value").alias("avg_neutral"))
    tweets_aggregated = tweets_aggregated.repartition(1)
    return tweets_aggregated

if __name__ == "__main__":
    # fixing a bug with this

    # create Spark session
    spark = SparkSession.builder.appName("AfDTweetAnalysis") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()

    #TODO change host for ICC
    host = socket.gethostbyname('socket-host-dns')
    #SRV = os.getenv('SERVER_ADDRESS')
    #host = "0.0.0.0"
    port = 5555
    # read the tweet data from socket
    lines = spark.readStream.format("socket") \
        .option("host", host) \
        .option("port", port)\
        .load()
    print("is Streaming: "+ str(lines.isStreaming))
    tweets = preprocessing(lines)
    tweets.printSchema()
    tweets_aggregated = aggregation(tweets)
    tweets = tweets.repartition(1)

    """
    query_view = tweets_aggregated.writeStream.queryName("all_tweets_view") \
        .outputMode("append") \
        .format("console") \
        .trigger(processingTime='120 seconds') \
        .start()
    """
    query_view = tweets_aggregated.writeStream.queryName("all_tweets_view") \
        .outputMode("append") \
        .format("mongodb") \
        .option("spark.mongodb.connection.uri", "mongodb://mongodb:27017/Big-Data-DB") \
        .option("spark.mongodb.database", "Big-Data-DB") \
        .option("checkpointLocation", "/checkpoints") \
        .option("spark.mongodb.collection", "TweetViews") \
        .trigger(processingTime="5 minutes") \
        .start()

    """
    query = tweets.writeStream.queryName("all_tweets") \
        .format("mongodb") \
        .option("spark.mongodb.connection.uri", "mongodb://mongodb:27017/Big-Data-DB") \
        .option("spark.mongodb.database", "Big-Data-DB") \
        .option("spark.mongodb.collection", "Tweets") \
        .option("checkpointLocation", "/checkpoints") \
        .outputMode("append") \
        .trigger(processingTime='60 seconds') \
        .start()
    """

    query_view.awaitTermination()
