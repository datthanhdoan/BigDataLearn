import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

# Database connection
SQLALCHEMY_DATABASE_URI = \
    f"postgresql://{os.environ.get('DATABASE_USER')}:" \
    f"{os.environ.get('DATABASE_PASSWORD')}@" \
    f"{os.environ.get('DATABASE_HOST')}:" \
    f"{os.environ.get('DATABASE_PORT')}/" \
    f"{os.environ.get('DATABASE_DB')}"

# Redis connection
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_CELERY_DB = os.environ.get('REDIS_CELERY_DB', 0)
REDIS_RESULTS_DB = os.environ.get('REDIS_RESULTS_DB', 1)

# Cấu hình bảo mật
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'your_secret_key_here') 