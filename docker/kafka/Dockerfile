# docker/kafka/Dockerfile
FROM wurstmeister/kafka:latest

# Copy custom configurations
COPY config/server.properties /opt/kafka/config/server.properties

# Expose Kafka port
EXPOSE 9092