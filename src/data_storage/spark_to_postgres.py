from sqlalchemy import create_engine, text
from pyspark.sql import SparkSession
import pandas as pd
from config.spark_config import SparkConfig

class SparkToPostgres:
    def __init__(self):
        try:
            # Thêm logging để debug
            print("Initializing SparkToPostgres...")
            
            # Thử kết nối PostgreSQL trước
            self.engine = create_engine('postgresql://superset:superset@postgres:5432/superset')
            
            # Test connection
            with self.engine.connect() as conn:
                print("Successfully connected to PostgreSQL")
                # Tạo bảng ngay sau khi kết nối thành công
                self.create_tables()
            
            # Khởi tạo Spark
            self.spark = SparkSession.builder \
                .appName(SparkConfig.APP_NAME) \
                .config("spark.jars", "/opt/spark/jars/postgresql-42.2.23.jar") \
                .getOrCreate()
                
            print("Successfully initialized Spark session")
            
        except Exception as e:
            print(f"Error in SparkToPostgres initialization: {e}")
            raise e

    def create_tables(self):
        try:
            with self.engine.connect() as conn:
                # Sử dụng text() để tránh SQL injection
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS covid_daily_stats (
                        timestamp TIMESTAMP,
                        country VARCHAR(100),
                        daily_cases INTEGER,
                        daily_deaths INTEGER,
                        daily_recovered INTEGER,
                        PRIMARY KEY (timestamp, country)
                    )
                """))

                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS covid_country_stats (
                        country VARCHAR(100) PRIMARY KEY,
                        total_cases INTEGER,
                        total_deaths INTEGER,
                        avg_cases FLOAT
                    )
                """))
                # Commit các thay đổi
                conn.commit()
                print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise e

    def save_to_postgres(self, spark_df, table_name, mode='append'):
        try:
            print(f"Attempting to save data to table: {table_name}")
            print(f"DataFrame schema: {spark_df.schema}")
            
            # Convert Spark DataFrame to Pandas
            pandas_df = spark_df.toPandas()
            print(f"Converted to Pandas DataFrame with shape: {pandas_df.shape}")
            
            # Save to PostgreSQL
            pandas_df.to_sql(
                table_name,
                self.engine,
                if_exists=mode,
                index=False,
                chunksize=1000
            )
            print(f"Successfully saved data to {table_name}")
            return True
        except Exception as e:
            print(f"Error saving to PostgreSQL: {e}")
            return False

    def close(self):
        if self.spark:
            self.spark.stop()
