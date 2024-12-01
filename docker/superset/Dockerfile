FROM apache/superset

USER root

# Cài đặt các dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python packages
RUN pip install psycopg2-binary redis

# Copy file cấu hình
COPY superset_config.py /app/pythonpath/superset_config.py

# Copy và cấp quyền cho entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER superset

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]