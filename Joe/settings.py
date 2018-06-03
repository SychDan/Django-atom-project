"""
Django settings for Joe project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5-7tc#boi&gm=rz%jwlc4qfp9l3#80-)z6n&oem32-z2njx5ha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Atom.apps.AtomConfig',
    'bootstrap3',
    'bootstrap4',
    'dj_pagination',
    'Atom.templatetags',
    'rest_framework',
    'el_pagination',
    'webpack_loader',
    'widget_tweaks',
    #'provider',
   #'provider.oauth2',
    'django.contrib.sites',
    'social_django',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ASGI_APPLICATION = "Atom.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'ROUTING': 'Atom.channels.channel_routing',
    },
}

SITE_ID=1

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

VK_APP_ID='6477162'
VKONTAKTE_APP_ID=VK_APP_ID
VK_API_SECRET='kb5YCGgUO5CbladbL3gJ'
VKONTAKTE_API_SECRET=VK_API_SECRET

SOCIAL_AUTH_TWITTER_KEY = 'tuUTknFllSbU6ThdSye0pVDgk'
SOCIAL_AUTH_TWITTER_SECRET = '151478LilNxKRdCNtodTPZtKamvIQRNqPquEptpGnVOFt1HFDp'

SOCIAL_AUTH_GITHUB_KEY='10be245c05bc014c3ab5'
SOCIAL_AUTH_GITHUB_SECRET='3c39e73a6d062eeda0137db381538621b712d39e'
SOCIAL_AUTH_GITHUB_REDIRECT_URL='http:127.0.0.1:8000/oauth/complete/github/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',

    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
  'social_core.pipeline.social_auth.social_details',
  'social_core.pipeline.social_auth.social_uid',
  'social_core.pipeline.social_auth.auth_allowed',
  'social_core.pipeline.social_auth.social_user',
  'social_core.pipeline.user.get_username',
  'social_core.pipeline.social_auth.associate_by_email',
  'social_core.pipeline.user.create_user',
  'social_core.pipeline.social_auth.associate_user',
  'social_core.pipeline.social_auth.load_extra_data',
  'social_core.pipeline.user.user_details',
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
STATICFILES_DIRS = (
    #This lets Django's collectstatic store our bundles
    os.path.join(BASE_DIR, 'assets'),
)

ROOT_URLCONF = 'Joe.urls'
AUTH_USER_MODEL = 'Atom.Person'

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
                'django.template.context_processors.request',


                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',

            ],
            'libraries':{
                'my_templatetag':'Atom.templatetags.mytags'
            }
        },
    },
]

WSGI_APPLICATION = 'Joe.wsgi.application'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_for_joe',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'default-character-set': 'utf-8',
        'default-server=set':'utf-8'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

DEBUG = True

if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)
   MIDDLEWARE_CLASSES = (
       'debug_toolbar.middleware.DebugToolbarMiddleware',
   )

   INSTALLED_APPS += (
       'debug_toolbar',
   )

   DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]

   DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
   }


#STATICFILES_FINDERS={
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
#}
STATIC_URL = '/static/'
#STATICFILES_DIRS=(os.path.join('/home/danny/PycharmProjects/Joe/','static'))
STATIC_ROOT ='/home/danny/PycharmProjects/Joe/static'
    #os.path.join(BASE_DIR, 'static')



try:
    from Joe.local_setting import *
except ImportError:
    pass