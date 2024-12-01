# Warning
This note is written in Vietnamese. It is my test note. It is not a guide, just a record of my tests.

### Tạo và kích hoạt môi trường ảo 

python -m venv venv
source venv/bin/activate  # Linux/Mac

hoặc

.\venv\Scripts\activate  # Windows

## Cài đặt các dependency
### Cần cài "Desktop development with C++" ,  Windows SDK và các công cụ C++ được tích
<!-- pip install --upgrade setuptools -->
pip install vs2015_runtime-14.40
pip install wheel setuptools

python-dateutil
pip install pyspark
pip install apache-superset
pip install psycopg2-binary
pip install sqlalchemy
pip install redis

pip install -r requirements.txt

## Build và khởi động các container
cd docker
docker-compose build
docker-compose up -d

### Kiểm tra Container đã chạy
docker ps

## Khởi tại superset
### Tạo admin user
 docker exec -it covid19_superset superset fab create-admin 
docker exec -it covid19_superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin

### Khởi tạo database
docker exec -it covid19_superset superset db upgrade

### Khởi tạo roles và permissions
docker exec -it covid19_superset superset init

## Kết nối các containers vào network
docker network connect covid19_net covid19_superset
docker network connect covid19_net superset_postgres
docker network connect covid19_net covid19_kafka
docker network connect covid19_net covid19_zookeeper
docker network connect covid19_net superset_redis
## Kiểm tra kết nối network:

docker network inspect covid19_net


### Đảm bảo port 9092 không bị sử dụng bởi process khác

netstat -ano | findstr :9092


## Kiểm tra Kafka đã hoạt động
### Liệt kê topics
docker exec covid19_kafka kafka-topics.sh --list --bootstrap-server localhost:9092

### Tạo topic test
docker exec covid19_kafka kafka-topics.sh --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1



## Khởi chạy
<!-- python src/main.py --mode both ( chạy ở / ) -->
docker exec -it covid19_spark python3 /opt/spark/apps/src/main.py --mode both


## Xem thông tin
http://localhost:8088/


## DEBUG
## Kết nối vào PostgreSQL
docker exec -it superset_postgres psql -U superset -d superset