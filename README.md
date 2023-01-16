# big-data
this is our code for our big data masters project. This repository is just a copy of our actual repository which is not accessible anymore.



### some notes
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
Deploy in Kubernetes
```
Deploy -> deply.yaml
If master is running check ip adress with:
kubectl get pods -o wide
add the ip adress of spark master to spark-worker env. SPARK_MASTER
Deploy -> spark-worker


start twitter socket stream:
kubectl exec <pod/sparkmaster> -c spark-master -- /spark/bin/spark-submit --conf "spark.driver.host=IP.Sparkmaster" --packages org.mongodb.spark:mongo-spark-connector:10.0.5 --master spark://<spark-master(ohne pod/)>:7077 /opt/spark-data/read_tweets.py


kubectl port-forward pod/mongodb-6f4484d7d8-5ch65 27017:27017
Connect MongoCompass with localhost:27017
```
