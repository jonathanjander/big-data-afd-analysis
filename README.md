# big-data



## Getting started
1. Baue twitter image streaming image falls nicht vorhanden.
```
# in /spark_streaming/twitter-streaming
docker build -t twitter-socket-stream . 
```
2. Container starten
```
docker-compose up -d
```
3. Stream starten
```
docker exec spark-master /spark/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector:10.0.5 --master spark://spark-master:7077 /opt/spark-data/read_tweets.py
```
Weitere hilfereiche commands
```
# mongo db
docker exec -it mongodb mongosh # mongo shell
docker exec -it mongodb bash # mongo bash
# spark
docker exec -it spark-master bash # spark bash
```