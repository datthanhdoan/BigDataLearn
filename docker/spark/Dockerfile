FROM apache/spark:3.5.0

USER root

# Cài đặt Python, pip và git
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    iputils-ping \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục cho apps và data
RUN mkdir -p /opt/spark/apps/src /opt/spark/data

# Copy source code và requirements
COPY src/ /opt/spark/apps/src/
COPY requirements.txt /opt/spark/apps/

# Cài đặt Python dependencies
WORKDIR /opt/spark/apps
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy PostgreSQL JDBC driver
ADD https://jdbc.postgresql.org/download/postgresql-42.2.23.jar /opt/spark/jars/

# Đảm bảo quyền truy cập
RUN chown -R spark:spark /opt/spark

# Thiết lập biến môi trường
ENV SPARK_HOME=/opt/spark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH
ENV PATH=$PATH:$SPARK_HOME/bin:/usr/local/bin:/usr/bin

# Kiểm tra cấu trúc thư mục và quyền
RUN ls -la /opt/spark/apps/src && \
    python3 --version && \
    which python3

USER spark

# Command mặc định
CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.master.Master"]