# Sentify - A real-time sentiment analysis pipeline for android app developers

## Dependencies
1. docker
2. docker-compose
3. selenium
4. confluent-kafka
5. textblob
6. pyspark
7. chromedriver

## Deployment Instructions
1. run `pip install docker docker-compose selenium confluent_kafka pyspark` if required.
2. use a text editor to create a docker-compose.yml such as `nvim docker-compose.yml` to write script to define containers.\
   you require the following services:
   * 01 x Zookeeper (port 2181)
   * 02 x Kafka Brokers (kafka1, kafka2) (port 29092)
   * 01 x Kafka UI (port 8080)
   * 01 x MongoDB (mongo v.4.4.5) (port 27017)
   * 01 x Metabase (v.0.47.10) (port 3000)
   * 01 x Postgres
3. create and run docker containers with `docker-compose up -d`
4. run `docker ps`/`docker-compose ps` to make sure all containers are running.
5. check whether containers are on the same network with `docker network ls` and `docker network inspect <target network>`.
6. make sure google-chrome and compatible chromedriver is installed in your system.
7. write the producer script called `selenium_producer.py` to use selenium and scrape review data and send to the message queue of kafka brokers.
8. write the consumer script called `consumer.py` to instruct spark-workers to process the data from the message queues, structure using PySpark and write to MongoDB.
9. copy `consumer.py` into spark-master container using `docker cp consumer.py <container_name/container-id>:/opt/bitnami/spark`.
10. perform the following checks:
    * access `<instance ip/localhost>:3000` to access metabase admin ui and connect to mongodb.
    * access `<instance ip/localhost>:8080` to access kafka spark-master ui to ensure spark-workers are linked to spark-master.
    * access `<instance ip/localhost>:8085` to access kafka cluster ui to ensure brokers are linked to cluster.
11. login to spark-master with `docker exec -it <container_name/container-id> bash` and install textblob with `pip install textblob`
12. run `spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/bitnami/spark/consumer.py` to run consumer script with dependencies.
13. access kafka spark-master ui to check if spark-worker nodes are being utilized.
14. run the producer script with `python selenium_producer.py`
15. access kafka cluster ui to check if the data is going into kafka topics. 
16. wait for data scraping and processing to finish.
17. access metabase ui to check data and perform visualizations.

## Work-in-progress
1. migration into aws cloud.
2. replace docker-compose with kubernetes to simulate large scale projects.
3. use github actions for CI/CD
4. Dynamic selection of url source
5. Simple flask UI
