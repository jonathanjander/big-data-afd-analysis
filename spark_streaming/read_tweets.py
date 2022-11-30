from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import os
import sys

#from scipy.sparse import spmatrix
#from textblob_de import TextBlobDE
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
    #sentiment_detection_udf = udf(core_nlp_sentiment_detection, ArrayType(StringType()))
    tweets = tweets.withColumn("sentiment", sentiment_detection_udf('tweet'))
    return tweets

def sentiment_detection(text):
    # old way (not good)
    #return TextBlobDE(text).sentiment.polarity

    # way too computationally expensive, we should do the sentiment calculation at a later state
    model = SentimentModel()
    classes, probabilities = model.predict_sentiment([text], output_probabilities=True)
    return [str(classes), str(probabilities)]


    # for testing
    #return ['test', 'test']


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
    os.environ['PYSPARK_PYTHON'] = './environment/bin/python'
    os.environ['PYSPARK_DRIVER_PYTHON'] = './environment/bin/python'
    #os.environ['PYSPARK_PYTHON'] = 'python3'
    #os.environ['PYSPARK_DRIVER_PYTHON'] = 'python3'
    #os.environ['PYSPARK_PYTHON'] = sys.executable
    #os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    # create Spark session
    spark = SparkSession.builder.appName("afd-tweet-analyzer-stream") \
        .config('spark.archives', 'pyspark_venv.tar.gz#environment') \
        .master('spark://localhost:7077') \
        .getOrCreate()
        #.master('spark://localhost:7077') \
        #.config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.5') \

        #.config("spark.mongodb.input.uri", "mongodb://127.0.0.1/afd_tweet_analyzer.tweets") \
        #.config("spark.mongodb.output.uri", "mongodb://127.0.0.1/afd_tweet_analyzer.tweets") \


    #spark.sparkContext.addPyFile("german_sentiment.zip")
    #spark.sparkContext.addPyFile("transformers-4.24.0-py3-none-any.zip")

    print('PYSPARK VERSION: '+spark.version)
    print('PYTHON VERSION: ' + sys.version)
    # read the tweet data from socket
    lines = spark.readStream.format("socket") \
        .option("host", "127.0.0.1") \
        .option("port", 5555)\
        .load()
    print("is streaming:" + str(lines.isStreaming))
    tweets = preprocessing(lines)
    tweets = sentiment(tweets)
    #tweets.printSchema()
    #create_table(tweets, spark)
    tweets = tweets.repartition(1)
    # encoding still doesn't work
    """
    query = tweets.writeStream.queryName("all_tweets") \
        .format("mongodb") \
        .option("spark.mongodb.connection.uri", "mongodb://localhost:27017/afd_tweet_analyzer") \
        .option("spark.mongodb.database", "afd_tweet_analyzer") \
        .option("spark.mongodb.collection", "tweets") \
        .option("checkpointLocation", "../data-warehouse/check") \
        .outputMode("append") \
        .trigger(processingTime='60 seconds') \
        .start()
    """
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
