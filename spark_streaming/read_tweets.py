from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import socket
import os
import sys

#import sparknlp
#from sparknlp.pretrained import PretrainedPipeline
#from scipy.sparse import spmatrix
#from textblob_de import TextBlobDE
#from datetime import datetime
#from germansentiment import SentimentModel

# TODO
# encode die tweets vollständig -> nur problem bei parquet files
# speicher sentiment und probability DONE
# speicher timestamps & eventuell auch link zum tweet DONE
# speicher in db
# filter nach sprache
def preprocessing(tweets_pre):
    # splits input string into tweets and timestamps (semicolon seperated)
    tweets_pre = tweets_pre.withColumn('tmp', split(col("value"), ';')).withColumn('tweet', col('tmp')[0]).withColumn('timestamp', col('tmp')[1]).withColumn('sentiment', col('tmp')[2]).withColumn('sentiment_probabilities', col('tmp')[3]).drop('tmp', 'value')
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', r'http\S+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', '@\w+', ''))
    tweets_pre = tweets_pre.withColumn('tweet', F.regexp_replace('tweet', 'RT:', ''))
    tweets_pre = tweets_pre.na.replace('', None)
    tweets_pre = tweets_pre.na.drop()
    return tweets_pre

#def new_sentiment_detection(tweets):
#    pipeline = PretrainedPipeline("classifierdl_bert_sentiment_pipeline", lang="de")
#    result = pipeline.annotate(
#        "Spiel und Meisterschaft nicht spannend genug? Muss man jetzt den Videoschiedsrichter kontrollieren? Ich bin entsetzt...dachte der darf nur bei krassen Fehlentscheidungen ran. So macht der Fussball keinen Spass mehr.")
#    return [str(result),'sfsadf']

def sentiment(tweets):
    sentiment_detection_udf = udf(sentiment_detection, ArrayType(StringType()))
    tweets = tweets.withColumn("sentiment", sentiment_detection_udf('tweet'))
    return tweets


def sentiment_detection(text):
    # old way (not good)
    #return TextBlobDE(text).sentiment.polarity

    # way too computationally expensive, we should do the sentiment calculation at a later state
    #model = SentimentModel()
    #classes, probabilities = model.predict_sentiment([text], output_probabilities=True)
    #return [str(classes), str(probabilities)]

    return ['test','test']

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

    # create Spark session
    spark = SparkSession.builder.appName("AfDTweetAnalysis") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()

        # .config("spark.jars.packages", "com.stratio.datasource:spark-mongodb_2.11:0.12.0") \
        # .config("spark.archives", "opt/spark-data/pyspark_venv.tar.gz#environment") \
        # .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.5') \


        #.config("spark.mongodb.input.uri", "mongodb://127.0.0.1/afd_tweet_analyzer.tweets") \
        #.config("spark.mongodb.output.uri", "mongodb://127.0.0.1/afd_tweet_analyzer.tweets") \
    host = socket.gethostbyname('socket-host-dns')
    port = 5555
    # read the tweet data from socket
    lines = spark.readStream.format("socket") \
        .option("host", host) \
        .option("port", port)\
        .load()
    print("is Streaming: "+ str(lines.isStreaming))
    tweets = preprocessing(lines)
    #tweets = sentiment(tweets)
    #tweets.printSchema()
    #create_table(tweets, spark)
    tweets = tweets.repartition(1)
    # encoding still doesn't work
    """
    query = tweets.writeStream.queryName("all_tweets") \
        .format("json") \
        .option("path", "../data-warehouse/json_files") \
        .option("checkpointLocation", "/checkpoints") \
        .option("encoding", 'UTF-8') \
        .trigger(processingTime='60 seconds') \
        .start()
        # .outputMode('append')

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
