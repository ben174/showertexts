import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# environment variable overrides this in production, yo
SECRET_KEY = 'i&s4g$@%7ql$3605y+2xw8w$*v-)p8kz5#8wch%h3jxvs*i@tn'

DEBUG = False

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if 'DB_NAME' in os.environ.keys():
    # running in production
    print '********** PRODUCTION *************'
    DEBUG = True
    ALLOWED_HOSTS = [
        '.showertexts.com', # Allow domain and subdomains
        'www.showertexts.com', # Allow domain and subdomains
        '.showertexts.com.', # Also allow FQDN and subdomains
    ]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
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
ENABLE_SHOWERBOT = True
REDDIT_CLIENT_ID = 'H22tb93fZSNgTg'
REDDIT_SECRET = ''

# a user agent string to identify ourselves to Reddit
REDDIT_USER_AGENT = 'ShowerTexts by /u/ben174 - http://www.showertexts.com'

# old style auth
REDDIT_USERNAME = 'showertexts'
REDDIT_PASSWORD = ''

# ***********************************


# override local vars with env vars, if they exist
TWILIO_SID = os.environ.get('TWILIO_SID', '')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN', '')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '')
TRIGGER_PASSWORD = os.environ.get('TRIGGER_PASSWORD', 'none')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET', '')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD', '')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
