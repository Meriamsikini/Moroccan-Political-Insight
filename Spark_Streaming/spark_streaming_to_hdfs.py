"""
PySpark script to consume tweets from a Kafka topic, clean the hashtags and spaces,
and then store the result in HDFS. The sensitive parameters (Kafka address, HDFS path) need to be filled in.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col, from_json
from pyspark.sql.types import StructType, StringType

# 1. Create the Spark session
spark = SparkSession.builder \
    .appName("CleanTweetsFromKafka") \
    .getOrCreate()

# 2. Read the Kafka topic (VM address to be completed)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "") \
    .option("subscribe", "json-topic") \
    .load()

# 3. Extract the JSON text 
tweets = df.selectExpr("CAST(value AS STRING) as json")

#4. Convert to a structured DataFrame 
schema = StructType().add("text", StringType())
tweets_df = tweets.select(from_json(col("json"), schema).alias("data")).select("data.text")

# 5. Clean the text: remove hashtags and spaces
cleaned = tweets_df.withColumn(
    "cleaned_text",
    regexp_replace(col("text"), r"#\w+", "")
).withColumn(
    "cleaned_text",
    regexp_replace(col("cleaned_text"), r"\s+", " ")
).withColumn(
    "cleaned_text",
    regexp_replace(col("cleaned_text"), r"^\s+|\s+$", "")
)

# 6. Save in HDFS (complete the storage path of the file in HDFS)
query = cleaned.select("cleaned_text").writeStream \
    .format("json") \
    .option("path", "") \
    .option("checkpointLocation", "/tmp/cleaned_tweets_checkpoint") \
    .outputMode("append") \
    .start()

query.awaitTermination()