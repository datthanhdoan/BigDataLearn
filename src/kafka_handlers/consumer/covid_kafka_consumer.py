from kafka import KafkaConsumer
import json
import logging
from spark_processors.covid_spark_processor import CovidSparkProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CovidDataConsumer:
    def __init__(self, bootstrap_servers='kafka:9092', topic_name='covid_data'):
        try:
            self.consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers=[bootstrap_servers],
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='covid_consumer_group'
            )
            self.spark_processor = CovidSparkProcessor()
            logger.info("Kafka consumer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Kafka consumer: {e}")
            raise e

    def process_data(self, data):
        try:
            logger.info(f"Processing data for {data['country']}")
            self.spark_processor.process_covid_data([data])
        except Exception as e:
            logger.error(f"Error processing data: {e}")

    def consume_messages(self):
        try:
            logger.info("Starting to consume messages...")
            for message in self.consumer:
                try:
                    data = message.value
                    logger.info(f"Received message: {data}")
                    
                    # Kiểm tra và xử lý dữ liệu
                    if not isinstance(data, dict):
                        logger.warning(f"Invalid message format: {data}")
                        continue
                    
                    # Kiểm tra các trường bắt buộc
                    required_fields = ['country', 'timestamp', 'cases', 'deaths']
                    if not all(field in data for field in required_fields):
                        logger.warning(f"Missing required fields: {data}")
                        continue
                    
                    # Xử lý dữ liệu với tên trường gốc
                    self.spark_processor.process_covid_data(data)
                    logger.info(f"Successfully processed data for {data['country']}")
                    
                except Exception as e:
                    logger.error(f"Error consuming messages: {str(e)}")
                    continue
        except Exception as e:
            logger.error(f"Error in consume_messages: {str(e)}")
            raise e
            
    def stop(self):
        if self.consumer:
            self.consumer.close()
        if hasattr(self, 'spark_processor'):
            self.spark_processor.stop()