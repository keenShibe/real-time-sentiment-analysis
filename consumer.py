from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StringType, StructType, StructField, IntegerType
from textblob import TextBlob

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingSentimentAnalysis") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/db.review_dev") \
    .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9093") \
  .option("subscribe", "reviewTopic") \
  .load()

schema = StructType([
    StructField("name", StringType(), True),
    StructField("date", StringType(), True),
    StructField("message", StringType(), True),
    StructField("star", IntegerType(), True),
])

json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("value")
)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

sentiment_udf = udf(analyze_sentiment, StringType())

message = json_df.select(
    col("value.name").alias("name"),
    col("value.message").alias("message"),
    col("value.date").alias("date"),
    col("value.star").alias("star"),
).withColumn("sentiment", sentiment_udf(col("message")))

query = message.writeStream.foreachBatch(lambda df, _: df.write.format("mongo").mode("append").save()).start()
query.awaitTermination()

