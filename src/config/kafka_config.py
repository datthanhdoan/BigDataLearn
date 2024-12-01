class KafkaConfig:
    BOOTSTRAP_SERVERS = 'localhost:9092'
    COVID_TOPIC = 'covid_data'
    GROUP_ID = 'covid_data_group'
    
    # Producer configs
    PRODUCER_CONFIG = {
        'bootstrap_servers': BOOTSTRAP_SERVERS,
        'acks': 'all',
        'retries': 3,
        'max_in_flight_requests_per_connection': 1,
        'api_version': (0, 10, 1)
    }
    
    # Consumer configs
    CONSUMER_CONFIG = {
        'bootstrap_servers': BOOTSTRAP_SERVERS,
        'group_id': GROUP_ID,
        'auto_offset_reset': 'latest',
        'enable_auto_commit': True,
        'auto_commit_interval_ms': 1000,
        'api_version': (0, 10, 1)
    }