#!/bin/bash
set -eo pipefail

echo "Initializing Superset..."

# Đợi PostgreSQL
echo "Waiting for postgres database to be ready..."
until PGPASSWORD=$DATABASE_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_DB" -c '\q'; do
    echo "Postgres is unavailable - sleeping"
    sleep 2
done

# Đợi Redis
echo "Waiting for redis to be ready..."
until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
    echo "Redis is unavailable - sleeping"
    sleep 2
done

echo "Upgrading DB..."
superset db upgrade

echo "Creating admin user..."
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin || true

echo "Initializing..."
superset init || true

echo "Starting Superset..."
gunicorn \
    --bind "0.0.0.0:8088" \
    --workers 2 \
    --timeout 120 \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    "superset.app:create_app()" 