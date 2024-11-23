# main.py
from src.kafka_handlers.producer.covid_kafka_producer import CovidDataProducer


if __name__ == "__main__":
    # Start producer
    producer = CovidDataProducer()
    producer.produce_messages()

    # In a separate process/terminal:
    # consumer = CovidDataConsumer()
    # consumer.consume_messages()