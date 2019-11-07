from .base import *

DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = [
    'habolt-frontend-dev.us-east-1.elasticbeanstalk.com',
    'http://habolt-frontend-dev.us-east-1.elasticbeanstalk.com/',
    'landing.habolt.mx',
    'habolt.mx'
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        " standard": {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },
    "handlers": {
        "analyzer": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/opt/python/log/analyzer.log",
            "formatter": "standard",
        },

    },
    "loggers": {
        "analyzer": {
            "handlers": ["analyzer"], "level": "DEBUG", "propagate": True
        },
        '': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

STRIPE_PUBLIC_KEY = config('STRIPE_LIVE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')
