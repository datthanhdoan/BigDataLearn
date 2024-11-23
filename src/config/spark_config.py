import os
import findspark

# Khởi tạo Spark
findspark.init()

class SparkConfig:
    SPARK_MASTER = "local[*]"
    APP_NAME = "CovidDataProcessor"
    
    # Cấu hình cho Windows
    SPARK_CONFIGS = {
        "spark.executor.memory": "2g",
        "spark.driver.memory": "2g",
        "spark.sql.shuffle.partitions": "10",
        "spark.default.parallelism": "4",
        "spark.driver.host": "localhost"  # Quan trọng cho Windows
    }
    
    # Đường dẫn Windows style
    HADOOP_HOME = os.path.join(os.environ.get('SPARK_HOME', ''), 'hadoop')
    os.environ['HADOOP_HOME'] = HADOOP_HOME