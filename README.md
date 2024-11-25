![Sentify](https://github.com/user-attachments/assets/57740589-e684-437f-b3d6-c28f0276f150)
# Sentify - A real-time sentiment analysis pipeline for android app developers

## Dependencies
1. docker
2. docker-compose
3. selenium
4. confluent-kafka
5. textblob
6. pyspark
7. chromedriver
8. streamlit

## Deployment Instructions
1. run `pip install docker docker-compose selenium confluent_kafka pyspark streamlit` if required.
2. create and run docker containers with `docker-compose up -d`
3. run `docker ps`/`docker-compose ps` to make sure all containers are running.
4. check whether containers are on the same network with `docker network ls` and `docker network inspect <target network>`.
5. make sure google-chrome and compatible chromedriver is installed in your system.
6. perform the following checks:
    * access `<instance ip/localhost>:3000` to access metabase admin ui and connect to mongodb.
    * access `<instance ip/localhost>:8080` to access kafka spark-master ui to ensure spark-workers are linked to spark-master.
    * access `<instance ip/localhost>:8085` to access kafka cluster ui to ensure brokers are linked to cluster.
7. login to spark-master with `docker exec -it <container_name/container-id> bash` and run `spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/bitnami/spark/consumer.py` to run consumer script with dependencies.
8. access kafka spark-master ui to check if spark-worker nodes are being utilized.
9. access streamlit ui and enter target url to scrape.
10. access kafka cluster ui to check if the data is going into kafka topics. 
11. wait for data scraping and processing to finish.
12. access metabase ui to check data and perform visualizations.
