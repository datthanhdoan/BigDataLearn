from venv import logger
from kafka import KafkaProducer
import json
import time
import requests
from datetime import datetime

class CovidDataProducer:
    def __init__(self, bootstrap_servers='kafka:9092', topic_name='covid_data'):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[bootstrap_servers],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            self.topic_name = topic_name
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Kafka producer: {e}")
            raise e

    def fetch_covid_data(self):
        """
        Fetches COVID-19 data from an API
        In this example, we're using a sample API - you should replace with your preferred data source
        """
        try:
            # Example API endpoint - replace with your actual data source
            response = requests.get('https://disease.sh/v3/covid-19/countries')
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def produce_messages(self):
        while True:
            try:
                covid_data = self.fetch_covid_data()
                if covid_data:
                    for country_data in covid_data:
                        message = {
                            'timestamp': datetime.now().isoformat(),
                            'country': country_data['country'],
                            'cases': country_data['cases'],
                            'deaths': country_data['deaths'],
                            'recovered': country_data.get('recovered', 0),  # Thêm get() với giá trị mặc định
                            'active': country_data.get('active', 0)
                        }
                        
                        future = self.producer.send(self.topic_name, message)
                        # Thêm callback để kiểm tra kết quả
                        future.add_callback(self._on_send_success)
                        future.add_errback(self._on_send_error)
                    
                    logger.info(f"Sent data batch at {datetime.now()}")
                time.sleep(300)  # 5 phút
            except Exception as e:
                logger.error(f"Error in produce_messages: {e}")
                time.sleep(60)  # Đợi 1 phút trước khi thử lại

    def _on_send_success(self, record_metadata):
        logger.info(f"Successfully sent message to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

    def _on_send_error(self, excp):
        logger.error(f"Error sending message: {excp}")

    def process_and_send_data(self, data):
        try:
            # Đảm bảo data có đúng format
            processed_data = {
                'country': data.get('country', ''),
                'timestamp': data.get('timestamp', ''),
                'cases': data.get('cases', 0),
                'deaths': data.get('deaths', 0),
                'recovered': data.get('recovered', 0),
                'active': data.get('active', 0)
            }
            
            # Log dữ liệu trước khi gửi
            logger.info(f"Sending data: {processed_data}")
            
            # Gửi dữ liệu
            self.producer.send(self.topic_name, value=processed_data)
            self.producer.flush()
            
            logger.info(f"Successfully sent data for {processed_data['country']}")
        except Exception as e:
            logger.error(f"Error processing and sending data: {e}")
            raise e

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],  # Thay đổi từ 'localhost:9092' thành 'kafka:9092'
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Gửi message test
test_message = {"test": "message"}
producer.send('covid_data', test_message)
producer.flush()
