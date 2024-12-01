# Requirements
- Docker Desktop
# Note 
This project does not use the lastest versions of kafka, spark, and superset (at the time of writing this - 11/2024) to ensure stability.
# Build and start containers
cd docker
docker-compose build
docker-compose up -d

# Open superset
http://localhost:8088/