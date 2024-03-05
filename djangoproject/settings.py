# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy
import os
import environ

# from django.urls import reverse

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.join(__file__, os.pardir))))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, 'external.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xmo&z@u0(dfbq!w(dl_0a^f(s9ukugs%id3)i(ei=$oxg%ir80'

DEBUG = env('DEBUG')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file':  os.path.join(BASE_DIR, 'my.cnf'),
        },
    }
}


ALLOWED_HOSTS = ['*']

# '18.221.173.7','127.0.0.1:8000'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'rest_framework',
    'courses',
    'app_teachers',
    'students',
    'app_quiz',
    'app_chat',
    'app_admin',
    'app_public',
    'app_cart',
    'app_students',
    'app_business',
    'embed_video',
    'app_api',
    'app_api_v2',
    'drf_yasg',
    'corsheaders'
)

MIDDLEWARE = [
    'compression_middleware.middleware.CompressionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'djangoproject.urls'

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

# WSGI_APPLICATION = 'wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'djangoproject/static'),
    os.path.join(BASE_DIR, 'static/'),
)

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')


# from django.core.urlresolvers import reverse_lazy
# from django.core.urlresolvers import reverse
LOGIN_REDIRECT_URL = reverse_lazy('course_list')
AUTH_USER_MODEL = "students.User"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGOUT_REDIRECT_URL = '/'

# APPEND_SLASH= False

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
             'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'debug_error.log',
            'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.ionos.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mail@pdhsafety.com'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

PAYPAL_CLIENT_ID_SANDBOX = 'AfCYO-690TOTak5bLJ9lxaw-a7nY-8SBFID1X7a6Cmoyw2X4j79OMSm7ZDp_6oj218W5YKF19qqgWW0Y&currency=USD&disable-funding=paylater'
PAYPAL_CLIENT_ID = 'AUlOGRZ6XAwhUIs2tDNy5-oTghhr9tW8NC9uCdDeh0LSMAwQVGxy4zWPyFRFmsXF1bSV7ZHVAm3mxCzu&currency=USD&disable-funding=paylater'