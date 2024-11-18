import logging
import openai

from dotenv import load_dotenv
from email.policy import default
from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

env = Env()

SECRET_KEY: str = env('DJANGO_SECRET_KEY')

DEBUG: bool = env.bool('DEBUG_MODE', default=False)

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']
else:
    STATICFILES_DIRS = []

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT: str = str(BASE_DIR / 'media')

LIST_DELIMITER: str = env('LIST_DELIMITER', default=',')

ALLOWED_HOSTS: list = env.list('ALLOWED_HOSTS', delimiter=LIST_DELIMITER)

CSRF_TRUSTED_ORIGINS: list = env.list('CSRF_TRUSTED_ORIGINS', delimiter=LIST_DELIMITER)

# OPENAI settings ------------------------
OPENAI_API_KEY = env('OPENAI_API_KEY')
# ----------------------------------------

# Logger settings ------------------------
LOGGER_DEBUG_LEVEL = logging.ERROR
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_NAME: str = env('PROJECT_NAME')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': (
                '-------------------------------------------------------\n'
                '%(asctime)s - %(levelname)s - %(message)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': LOGGER_DEBUG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / f'{PROJECT_NAME}.log',
            'formatter': 'custom',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGGER_DEBUG_LEVEL,
            'propagate': True,
        },
    },
}
# ----------------------------------------

INSTALLED_APPS = [
    # local apps --------------
    'analyzing.apps.AnalyzingConfig',
    'api.apps.ApiConfig',
    'management.apps.ManagementConfig',
    # -------------------------
    # Third-party apps --------
    'drf_yasg',
    'corsheaders',
    # -------------------------
    # Project apps ------------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'adrf',
    # -------------------------
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = ('management.backends.users.CaseInsensitiveModelBackend',)

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'settings.wsgi.application'

# Database settings ----------------------
DATABASE_ENGINE = {
    0: {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    1: {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': env.int('POSTGRES_PORT', default=5432),
        'NAME': env('POSTGRES_NAME', default='postgres'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres'),
    },
}
DATABASES = {'default': DATABASE_ENGINE[env.int('DATABASE_ENGINE', default=0, choices=DATABASE_ENGINE.keys())]}
# ----------------------------------------

# Cache settings -------------------------
CACHE_ENGINES = {
    0: {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': f'{PROJECT_NAME}_CACHE_TABLE',
    },
    1: {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('CACHE_REDIS_URL', default='redis://127.0.0.1:6379'),
    },
}
CACHE_ENGINE = env.int('CACHE_ENGINE', default=0, choices=CACHE_ENGINES.keys())
CACHES = {'default': CACHE_ENGINES.get(CACHE_ENGINE, CACHE_ENGINES[0])}
# ----------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ]
}


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

# Celery settings ------------------------
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_URL')
# ----------------------------------------

SAFE_EXECUTE = env.bool('SAFE_EXECUTE', default=True)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
