# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'PORT': 5432,
        'NAME': "codingplatform",
        'USER': "codingplatform",
        'PASSWORD': 'codingplatform'
    }
}

REDIS_CONF = {
    "host": "redis",
    "port": "6379"
}


DEBUG = True

ALLOWED_HOSTS = ["*"]

DATA_DIR = f"{BASE_DIR}/data"
