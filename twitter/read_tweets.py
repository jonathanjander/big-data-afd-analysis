from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import os
import sys

from scipy.sparse import spmatrix
from textblob_de import TextBlobDE
from datetime import datetime
from germansentiment import SentimentModel

# TODO
# encode die tweets vollständig -> nur problem bei parquet files
# speicher sentiment und probability DONE
# speicher timestamps & eventuell auch link zum tweet DONE
# speicher in db
# filter nach sprache
def preprocessing(tweets_pre):
    # splits input string into tweets and timestamps (semicolon seperated)
    tweets_pre = tweets_pre.withColumn('tmp', split(col("value"), ';')).withColumn('tweet', col('tmp')[0]).withColumn('timestamp', col('tmp')[1]).drop('tmp', 'value')
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', r'http\S+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', '@\w+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', 'RT:', ''))
    tweets_pre = tweets_pre.na.replace('', None)
    tweets_pre = tweets_pre.na.drop()
    return tweets_pre


def sentiment(tweets):
    sentiment_detection_udf = udf(sentiment_detection, ArrayType(StringType()))
    tweets = tweets.withColumn("sentiment", sentiment_detection_udf('tweet'))
    return tweets


def sentiment_detection(text):
    # old way (not good)
    #return TextBlobDE(text).sentiment.polarity

    # way too computationally expensive, we should do the sentiment calculation at a later state
    model = SentimentModel()
    classes, probabilities = model.predict_sentiment([text], output_probabilities=True)
    return [str(classes), str(probabilities)]


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

def create_table(tweets_df, spark):

    tweets_df.createOrReplaceTempView('test')
    spark.sql("SELECT tweet FROM test").show()

if __name__ == "__main__":
    # fixing a bug with this
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    # create Spark session
    spark = SparkSession.builder.appName("AfDTweetAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "127.0.0.1").option("port", 5555).load()
    tweets = preprocessing(lines)
    tweets = sentiment(tweets)
    #tweets.printSchema()
    #create_table(tweets, spark)
    tweets = tweets.repartition(1)
    # encoding still doesn't work
    query = tweets.writeStream.queryName("all_tweets") \
        .format("json") \
        .option("path", "../data-warehouse/json_files") \
        .option("checkpointLocation", "../data-warehouse/check") \
        .option("encoding", 'UTF-8') \
        .trigger(processingTime='60 seconds') \
        .start()
        # .outputMode('append')

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
