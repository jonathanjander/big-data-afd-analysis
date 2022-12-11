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
Deploy in Kubernetes
```
Deploy -> service
kubectl apply -f service.yaml
Deploy -> spark-master
If master is running check ip adress with:
kubectl get pods -o wide
add the ip adress of spark master to spark-worker env. SPARK_MASTER
Deploy -> spark-worker
Deploy -> twitter
Deploy -> mongodb

start twitter socket stream:
kubectl exec pod/spark-master-5856cbdfcc-m7ccq -c spark-master -- /spark/bin/spark-submit --conf "spark.driver.host=10.233.87.114" --packages org.mongodb.spark:mongo-spark-connector:10.0.5 --master spark://spark-master-5856cbdfcc-m7ccq:7077 /opt/spark-data/read_tweets.py


kubectl port-forward pod/mongodb-74b4c8b5f5-2w9wf 27017:27017
Connect MongoCompass with localhost:27017
```