from pyspark.sql import SparkSession
import time
from textblob_de import TextBlobDE as textBlob
#download textblob https://www.nltk.org/data.html


def main():
    spark = SparkSession.builder.getOrCreate()
    newspaper_title = spark.read.csv('../data-warehouse/Schlagzeilen.csv', header=True)
    print(type(newspaper_title))
    newspaper_title.show()
    newspaper_title.select("content")
    # df = newspaper_title.rdd.map(lambda x: print(x.idcontent))

    tweets = spark.read.csv("../data-warehouse/Afd_tweets.csv", header=True)
    tweets.show()
    tweets.printSchema()
    #rdd = tweets.rdd.map(lambda x: textBlob(x).sentiment)
    #df = rdd.toDF()
    #df.show()
    text = "ich liebe Ostern"
    blob = textBlob(text)
    print(blob.sentences)
    print(blob.tokens)
    print(blob.sentiment)


if __name__ == '__main__':
    main()
