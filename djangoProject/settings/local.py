from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ovaas2_test',
        'USER': 'li',
        'PASSWORD': '123123',
        'HOST': 'localhost',

    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ovaas2_test',
#         'USER': 'ovaas_test_user@ovaas2',
#         'PASSWORD': 'password',
#         'HOST': 'ovaas2.mysql.database.azure.com',
#         'PORT': 3306,
#         # 'OPTIONS': {'ssl': {'ca': BASE_DIR/'db/BaltimoreCyberTrustRoot.crt.pem'}}
#     }
# }


# redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
