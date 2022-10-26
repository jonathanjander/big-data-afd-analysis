from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.getOrCreate()
    newspaper_title = spark.read.csv('../data-warehouse/Schlagzeilen.csv', header=True)
    newspaper_title.show()

    tweets = spark.read.csv("../data-warehouse/Afd_tweets.csv", header=True)
    tweets.show()


if __name__ == '__main__':
    main()
