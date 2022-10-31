from pyspark.sql import functions as f
from pyspark.sql.functions import *
# preprocessing of a tweet
"""
https://towardsdatascience.com/sentiment-analysis-on-streaming-twitter-data-using-spark-structured-streaming-python-fc873684bfe3
taken from part 2 tweet preprocessing
"""
def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', f.regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', f.regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', f.regexp_replace('word', '#', ''))
    words = words.withColumn('word', f.regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', f.regexp_replace('word', ':', ''))
    return words