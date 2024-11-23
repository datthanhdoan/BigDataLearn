# src/main.py
import argparse
from kafka_handlers.producer.covid_kafka_producer import CovidDataProducer
from kafka_handlers.consumer.covid_kafka_consumer import CovidDataConsumer
from utils.logger import setup_logger
import threading
import signal
import sys

logger = setup_logger('main')

def run_producer():
    producer = CovidDataProducer()
    try:
        producer.produce_messages()
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
        producer.stop()

def run_consumer():
    consumer = CovidDataConsumer()
    try:
        consumer.consume_messages()
    except KeyboardInterrupt:
        logger.info("Stopping consumer...")
        consumer.stop()

def run_both():
    producer_thread = threading.Thread(target=run_producer)
    consumer_thread = threading.Thread(target=run_consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()

def main():
    parser = argparse.ArgumentParser(description='COVID-19 Data Processing System')
    parser.add_argument('--mode', 
                       choices=['producer', 'consumer', 'both'],
                       default='both',
                       help='Run mode: producer, consumer, or both')
    
    args = parser.parse_args()
    
    if args.mode == 'producer':
        run_producer()
    elif args.mode == 'consumer':
        run_consumer()
    else:
        run_both()

if __name__ == "__main__":
    main()