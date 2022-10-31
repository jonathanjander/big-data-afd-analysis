import findspark

findspark.init('C:/Program Files/Apache Spark/spark-3.3.1-bin-hadoop3/spark-3.3.1-bin-hadoop3')

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc

from collections import namedtuple

import time
from IPython import display
import matplotlib.pyplot as plt
import seaborn as sns
import pandas

sc = SparkContext()
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

socket_stream = ssc.socketTextStream("127.0.0.1", 5556)
lines = socket_stream.window(20)

#sparkInstance = SparkSession.builder.appName("afdTweetAnalyzer").getOrCreate()
#lines = sparkInstance.readStream.format("socket").option("host", "127.0.0.1").option("port", 5556).load()

fields = ("tag", "count")
Tweet = namedtuple('tweets', fields)

# Use Parenthesis for multiple lines or use \.
(lines.flatMap(lambda text: text.split(" "))  # Splits to a list
 .filter(lambda word: word.lower().startswith("#"))  # Checks for hashtag calls
 .map(lambda word: (word.lower(), 1))  # Lower cases the word
 .reduceByKey(lambda a, b: a + b)  # Reduces
 .map(lambda rec: Tweet(rec[0], rec[1]))  # Stores in a Tweet Object
 .foreachRDD(lambda rdd: rdd.toDF().sort(desc("count"))  # Sorts Them in a DF
             .limit(10).registerTempTable("tweets")))  # Registers to a table.

ssc.start()

count = 0
while count < 10:
    time.sleep(3)
    top_10_tweets = sqlContext.sql('Select tag, count from tweets')
    top_10_df = top_10_tweets.toPandas()
    top_10_df.sort(desc("count"))
    print(top_10_df)
    #display.clear_output(wait=True)
    #plt.figure(figsize=(10, 8))
    #sns.barplot(x="count", y="keyword", data=top_10_df)
    #plt.show()
    count = count + 1
    print(count)

ssc.stop()
