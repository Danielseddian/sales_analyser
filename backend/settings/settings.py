import logging
from pathlib import Path
from dotenv import load_dotenv
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

env = Env()

SECRET_KEY: str = env('DJANGO_SECRET_KEY')

DEBUG: bool = env.bool('DEBUG_MODE', default=False)

if DEBUG:
    STATIC_ROOT: str = ''
    STATICFILES_DIRS: tuple = ((BASE_DIR / 'static'),)
else:
    STATIC_ROOT: str = str(BASE_DIR / 'static')

MEDIA_ROOT: str = str(BASE_DIR / 'media')

LIST_DELIMITER: str = env('LIST_DELIMITER', default=',')

ALLOWED_HOSTS: list = env.list('ALLOWED_HOSTS', delimiter=LIST_DELIMITER)

CSRF_TRUSTED_ORIGINS: list = env.list('CSRF_TRUSTED_ORIGINS', delimiter=LIST_DELIMITER)

# Logger settings ------------------------
LOGGER_DEBUG_LEVEL = logging.ERROR
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_NAME: str = env('PROJECT_NAME')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOGGER_DEBUG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / f'{PROJECT_NAME}.log',
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


INSTALLED_APPS = [
    # local apps --------------
    'management.apps.ManagementConfig',
    # -------------------------
    # Third-party apps --------
    # -------------------------
    # Project apps ------------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # -------------------------
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "settings.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
