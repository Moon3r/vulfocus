"""
Django settings for vulfocus project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import docker
import datetime
import redis
from django.core.management import utils

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except:
    SECRET_KEY = utils.get_random_secret_key()
    os.environ['SECRET_KEY'] = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = "user.UserProfile"

# Application definition
ALLOWED_IMG_SUFFIX = ["jpg", "jpeg", "png"]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user',
    'corsheaders',
    'dockerapi',
    'network',
    'tasks',
    'layout_image',
    'captcha',
    'notifications',
    'notice',
    'frp',
]

# redis host
REDIS_HOST = "127.0.0.1"
# redis port
REDIS_PORT = 6379
# redis pass
REDIS_PASS = ""
if REDIS_PASS:
    CELERY_BROKER_URL = "redis://:%s@%s:%s/0" % (REDIS_PASS, str(REDIS_HOST), str(REDIS_PORT))
    REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASS, decode_responses=True, db=1)
else:
    CELERY_BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, str(REDIS_PORT))
    REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True,db=1)

REDIS_IMG = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=6, decode_responses=True)
REDIS_USER_CACHE = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=7, decode_responses=True)

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_SERIALIZER = 'json'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:9527",
]
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

JWT_AUTH = {
    # 'JWT_RESPONSE_PAYLOAD_HANDLER':'user.jwt.jwt_response_payload_handler',
    # 指明token的有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_AUTH_HEADER_PREFIX': 'BMH',
}


ROOT_URLCONF = 'vulfocus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vulfocus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 默认启动容器最长时间为 60s，可根据实际情况调整
DOCKER_CONTAINER_TIME = 60

try:
    # DOCKER_URL tcp://127.0.0.1:2375 or unix://var/run/docker.sock
    # DOCKER_URL = "tcp://192.168.87.136:2375"
    # DOCKER_URL = os.environ['DOCKER_URL']
    DOCKER_URL = "unix:///var/run/docker.sock"
except:
    DOCKER_URL = "unix:///var/run/docker.sock"

if DOCKER_URL.startswith("unix:"):
    client = docker.DockerClient(base_url=DOCKER_URL)
    api_docker_client = docker.APIClient(base_url=DOCKER_URL)
else:
    client = docker.DockerClient(DOCKER_URL)
    api_docker_client = docker.APIClient(base_url=DOCKER_URL)

try:
    """
    设置 docker-compose 连接
    """
    os.environ['DOCKER_HOST'] = DOCKER_URL
except Exception as e:
    pass


# 靶场绑定 IP，提供用户访问靶场与 Docker 服务IP保持一致。
VUL_IP = ""
try:
    if os.environ['VUL_IP']:
        VUL_IP = os.environ['VUL_IP']
except Exception as e:
    pass

DOCKER_COMPOSE = os.path.join(BASE_DIR, "docker-compose")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
try:
    if os.environ['EMAIL_HOST']:
        EMAIL_HOST = os.environ['EMAIL_HOST']
    if os.environ['EMAIL_HOST_USER']:
        EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    if os.environ['EMAIL_HOST_PASSWORD']:
        EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
except Exception as e:
    pass

#邮箱配置
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = 465
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = True
EMAIL_FROM = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 字母验证码设置
CAPTCHA_IMAGE_SIZE = (90, 45)   # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4   # 字符个数
CAPTCHA_TIMEOUT = 1   # 过期时间(minutes)


COMPOSE_ZIP_PATH = os.path.join(BASE_DIR, "compose-zip-store")
# docker-compose文件下载格式
DOWNLOAD_FILE_TYPE = ".zip"
UPLOAD_ZIP_PATH = os.path.join(BASE_DIR, "upload_zip")