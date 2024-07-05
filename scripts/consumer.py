from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StringType, StructType, StructField, IntegerType
from textblob import TextBlob

# Create a SparkSession with the MongoDB configuration
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingSentimentAnalysis") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/db.review_dev") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Read the streaming data from Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:29093") \
  .option("subscribe", "reviewTopic") \
  .load()

# Define the schema for the JSON data
schema = StructType([
    StructField("name", StringType(), True),
    StructField("date", StringType(), True),
    StructField("message", StringType(), True),
    StructField("star", IntegerType(), True),
])

# Parse the JSON data
json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("value")
)

# Define a UDF for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

sentiment_udf = udf(analyze_sentiment, StringType())

# Add the sentiment analysis column to the DataFrame
message = json_df.select(
    col("value.name").alias("name"),
    col("value.message").alias("message"),
    col("value.date").alias("date"),
    col("value.star").alias("star"),
).withColumn("sentiment", sentiment_udf(col("message")))

# Define the write function to MongoDB
def write_to_mongo(df, epoch_id):
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("database", "db") \
        .option("collection", "review_dev") \
        .save()
    print(f"Batch {epoch_id} written to MongoDB")

# Write the streaming DataFrame to MongoDB using foreachBatch
query = message.writeStream.foreachBatch(write_to_mongo).start()
query.awaitTermination()
