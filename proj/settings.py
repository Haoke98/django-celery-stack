"""
Django settings for izBasar project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import logging
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from .simpleUISettings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
# Take environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')

CSRF_TRUSTED_ORIGINS = ['http://keeper.sdm.net', 'http://kept.sdm.net']
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'none'

LOG_FILE_DIR = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

PUBLIC_ROOT = os.path.join(BASE_DIR, 'public')
if not os.path.exists(PUBLIC_ROOT):
    os.mkdir(PUBLIC_ROOT)

STATIC_URL = "/static/"
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../'))
logging.debug("SITE_ROOT:{}", SITE_ROOT)

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')
logging.debug("STATIC_ROOT:{}", STATIC_ROOT)
if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder")
# 静态资源目录列表
# 注：当DEBUG=True时，Django将为开发环境提供静态资源服务，该服务将从这些文件夹中搜取静态资源。
# 注：当DEBUG=False时，Django将不会再启动静态资源，如果启动了静态资源，也将会从STATIC__ROOT文件夹中搜取静态资源。
# 注：当执行python manage.py collectstatic 命令时，将把STATICFILES__DIR中的所有静态资源复制到STATIC__ROOT中去
STATICFILES_DIRS = [

]
logging.debug("STATICFILES_DIR:{}", STATICFILES_DIRS)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, "media")
logging.debug("MEDIA_ROOT:{}", MEDIA_ROOT)
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

IMAGE_ROOT = os.path.join(MEDIA_ROOT, "img")
if not os.path.exists(IMAGE_ROOT):
    os.mkdir(IMAGE_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True
# FIXME 代码中敏感信息泄漏了, 赶紧处理一下
ADMINS = (('Sadam·Sadik', '1903249375@qq.com'),)  # 接受报错的账号
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER  # 必须要设置 不然logger中得handler：admin_Email 无法发送错误报告邮件，  SERVER_EMAIL必须和 EMAIL_HOST_USER一样才能成功发送
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "RESPONSE_HEADER_NAME"

########### Django Logging  BEGIN ##############
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'new_add': {
            '()': 'middlewares.RequestLogFilter',
        },

    },
    'formatters': {
        'standard': {
            # 这里使用filter request_id里的request_id字段
            'format': '[{asctime:s}][{levelname:^7s}][{processName:s}({process:d}):{threadName:s}({thread:d})][{source_ip}][{hostname}][{request_id}][{filename:s}:{lineno:d}:{funcName:s}]{message:s}',
            'style': '{',
        },
        'default': {
            'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['new_add', 'request_id'],
            'formatter': 'standard',  # 这里使用上面的formatter: standard
        },
        'file': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            'level': 'INFO',
            'filters': ['new_add', 'request_id'],
            'filename': os.path.join(LOG_FILE_DIR, 'AllKeeper.log'),  # 日志输出文件
            'formatter': 'standard',  # 使用哪种formatters日志格式
            'backupCount': 100,  # 备份份数
            'encoding': 'utf-8',

            # 按照时间切割
            'class': 'proj.log.CommonTimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,

            # 按照文件大小切割
            # 'class': 'logging.handlers.RotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 5,  # 文件大小
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,

        }
    },
    'root': {
        'handlers': ['console', 'file', 'mail_admins'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],  # 这里使用上面的handler: console
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        'icloud': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
##############    Django Logging  END   ##############


# Application definition
INSTALLED_APPS = [
    'simplepro',
    'simpleui',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'rest_framework',
    'corsheaders',
    'docutils',
    'sortedm2m',
    'django_crontab',
    'django_celery_beat',
    'django_celery_results',
    'django_celery_stack'
]
SITE_ID = 1
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_DIR,
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.RequestLogMiddleware',
    # 加入simplepro的中间件
    'simplepro.middlewares.SimpleMiddleware'
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'https://sdc.mldoo.com',
]
# 如果需要设置其他CORS参数，也可以在settings.py中进行配置
CORS_ALLOW_CREDENTIALS = True
# 允许发送的HTTP头
CORS_ALLOW_HEADERS = [
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
]

ROOT_URLCONF = 'proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # <-需要这一行
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'USER': os.getenv("DB_USERNAME"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'CONN_MAX_AGE': 0,
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        #     'use_unicode': True,
        # },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'zh-Hans'  # 'en-us'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = 'Asia/Shanghai'  # 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True  # true时统一全球时间，不跨时区的应用可以设为False

DATETIME_FORMAT = 'Y/m/d H:i:s'

DATE_FORMAT = 'Y/m/d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
FILE_CHARSET = 'gb18030'
DEFAULT_CHARSET = 'utf-8'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/css', '.min.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/html', '.html')

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "proj.pagination.StandardPagination",
    "PAGE_SIZE": 10
}

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
# 因为MINIO中不光存储静态资源还会存储动态资源,相对比较铭感,必须强制加密通信
MINIO_STORAGE_USE_HTTPS = True
MINIO_STORAGE_ENDPOINT = os.getenv('MINIO_STORAGE_ENDPOINT')
MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_STORAGE_ACCESS_KEY')
MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_STORAGE_SECRET_KEY')
MINIO_STORAGE_MEDIA_OBJECT_METADATA = {"Cache-Control": "max-age=1000"}
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'data-process-engine-media'
MINIO_STORAGE_MEDIA_BACKUP_BUCKET = 'data-process-engine-recycle-bin'
MINIO_STORAGE_MEDIA_BACKUP_FORMAT = '%c/'
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = 'data-process-engine-static'

# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_RESULT_BACKEND = "django_celery_stack.backends:CustomDatabaseBackend"
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_CACHE_BACKEND = "django-cache"

# celery升到5.3后使用原来的启动命令会出警告，加上这个配置后就不会了
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# 会减少Worker中任务执行时因通信和状态更新而引发的性能缩水, 但是会增加BROKER的负载, 很有可能出现宕机等状况.
# CELERY_BROKER_CONNECTION_MAX_RETRIES = None

FLOWER_UNAUTHENTICATED_API = True
