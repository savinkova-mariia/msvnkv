import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'qb0y7xz8@pu3izm6&hw0f$w*+n)xm6o3lz_uqp%@w*p@zk0q1u'

DEBUG = False

ALLOWED_HOSTS = ('localhost', 'msvnkv.com', )
INTERNAL_IPS = ('127.0.0.1', )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www/static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'www/files')

SITE_ID = 1

SESSION_COOKIE_DOMAIN = 'msvnkv.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

json_config_path = os.path.join(BASE_DIR, 'blog', 'local_settings.json')
if os.path.exists(json_config_path):
    with open(json_config_path) as f:
        json_config = json.loads(f.read())
        for param, value in json_config.items():
            setattr(sys.modules[__name__], param, value)

COMPRESS_ENABLED = not DEBUG
COMPRESS_OUTPUT_DIR = 'compress'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'compressor',
    'preferences',
    'martor',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.processors.settings_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

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

PAGINATION_PAGE_SIZE = 10

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Yekaterinburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',
    'mention': 'true',
    'jquery': 'true',
}

MARTOR_IMGUR_CLIENT_ID = 'd8a43ef54e17512'
MARTOR_IMGUR_API_KEY = 'c9f1a7991902aab1cd37cf8653254deec70aece0'

MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    'martor.extensions.urlize',
    'martor.extensions.emoji',
    'martor.extensions.mdx_video',
]

MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}
