
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from textblob_de import TextBlobDE as textBlob
#download textblob https://www.nltk.org/data.html
#newspaper_title_scraper
from newspaper_title_scraper import scrape_newspaper_title

def main():
    spark = SparkSession.builder.getOrCreate()
    spark_context = spark.sparkContext
    titles = scrape_newspaper_title()

    rdd_title = spark_context.parallelize(titles)
    titles_dict = rdd_title.map(lambda x: {"Title": x})
    rdd_filtered = rdd_title.filter(lambda x: x.contain("BILDplus"))
    rdd = rdd_filtered.collect()
    for i, row in enumerate(rdd):
        print(row)

    tweets = spark.read.csv("../data-warehouse/Afd_tweets.csv", header=True)
    tweets.show()
    tweets.printSchema()


if __name__ == '__main__':
    main()
