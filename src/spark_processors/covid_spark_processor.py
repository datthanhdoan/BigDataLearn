from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from data_storage.spark_to_postgres import SparkToPostgres
import logging
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

logger = logging.getLogger(__name__)

class CovidSparkProcessor:
    def __init__(self):
        try:
            self.spark = SparkSession.builder \
                .appName("CovidDataProcessor") \
                .config("spark.driver.host", "spark") \
                .config("spark.jars", "/opt/spark/jars/postgresql-42.2.23.jar") \
                .getOrCreate()
            self.postgres_storage = SparkToPostgres()
            logger.info("Spark processor initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Spark processor: {e}")
            raise e

    def process_covid_data(self, data):
        try:
            logger.info("Creating Spark DataFrame")
            # Định nghĩa schema
            schema = StructType([
                StructField("timestamp", StringType(), True),
                StructField("country", StringType(), True),
                StructField("cases", IntegerType(), True),
                StructField("deaths", IntegerType(), True),
                StructField("recovered", IntegerType(), True),
                StructField("active", IntegerType(), True)
            ])
            
            # Chuyển data thành list nếu không phải
            if not isinstance(data, list):
                data = [data]
            
            df = self.spark.createDataFrame(data, schema=schema)
            df.cache()

            # Daily statistics
            daily_stats = df.groupBy("timestamp", "country") \
                .agg(
                    sum("cases").alias("daily_cases"),
                    sum("deaths").alias("daily_deaths"),
                    sum("recovered").alias("daily_recovered")
                )

            # Country statistics
            country_stats = df.groupBy("country") \
                .agg(
                    sum("cases").alias("total_cases"),
                    sum("deaths").alias("total_deaths"),
                    avg("cases").alias("avg_cases")
                )

            logger.info("Saving to PostgreSQL")
            self.postgres_storage.save_to_postgres(daily_stats, "covid_daily_stats")
            self.postgres_storage.save_to_postgres(country_stats, "covid_country_stats")

        except Exception as e:
            logger.error(f"Error processing data: {e}")

    def stop(self):
        if self.spark:
            self.spark.stop() 