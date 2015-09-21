import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# environment variable overrides this in production, yo
SECRET_KEY = 'i&s4g$@%7ql$3605y+2xw8w$*v-)p8kz5#8wch%h3jxvs*i@tn'

# only for dev, env variable overrides in prod
DEBUG = True

ALLOWED_HOSTS = [
    '.showertexts.com'
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'texts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'showertexts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates','/opt/python/current/app/showertexts/templates'],
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

WSGI_APPLICATION = 'showertexts.wsgi.application'


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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# used to trigger daily text send job - overridden in prod via env variable
TRIGGER_PASSWORD = 'none'

# days until account is considered 'expired' - a notice is sent out and then the acct is set to inactive
EXPIRATION_DAYS = 14

TWILIO_NUMBER = '+14152002895'

# ***********************************
# Reddit showertexts bot settings  (showerbot.py)

# oauth
REDDIT_CLIENT_ID = 'H22tb93fZSNgTg'
REDDIT_SECRET = ''

# a user agent string to identify ourselves to Reddit
REDDIT_USER_AGENT = 'ShowerTexts by /u/ben174 - http://www.showertexts.com'

# old style auth
REDDIT_USERNAME = 'showertexts'
REDDIT_PASSWORD = ''

# ***********************************


if 'DJANGO_ADMIN_PASSWORD' in os.environ:
    ACCOUNT_SID = os.environ['TWILIO_SID']
    AUTH_TOKEN = os.environ['TWILIO_TOKEN']
    ADMIN_PASSWORD = os.environ['DJANGO_ADMIN_PASSWORD']
    TRIGGER_PASSWORD = os.environ['TRIGGER_PASSWORD']
    REDDIT_SECRET = os.environ['REDDIT_SECRET']
    REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
    DEBUG = bool(os.environ.get('DEBUG', False))

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")



# load custom settings if they exist. this looks anywhere in the path
try:
    from custom_settings import *
    print "Using custom_settings file."
except ImportError:
    pass
