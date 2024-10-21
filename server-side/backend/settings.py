"""
Django settings for backend project.
Generated by 'django-admin startproject' using Django 4.2.6.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import boto3
from datetime import timedelta
import os
from dotenv import load_dotenv
from  . import firebase_admin_setup
import json

DEBUG = os.getenv("DEBUG")

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
SECRET_KEY = os.getenv("SECURE_KEY")
FRONT_END_URL = os.getenv("FRONT_END_URL")
BACKEND_URL = os.getenv("BACKEND_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_TEST_MODE = os.getenv("STRIPE_TEST_MODE")
HF_TOKEN = os.getenv("HF_TOKEN")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_PRIVATE_KEY = os.getenv("STRIPE_PRIVATE_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if STRIPE_TEST_MODE:
    print("Stripe is in test mode")
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_TEST_KEY")
    STRIPE_PRIVATE_KEY = os.getenv("STRIPE_PRIVATE_TEST_KEY")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET_TEST")

if DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

HF_SERVER_FACELESS = ["otmanheddouch/faceless"]  # Change this to your hugging face space

redirect_uris = ["https://api.reelze.app/api/oauth2callback_yt", "http://localhost:8000/api/oauth2callback_yt"]
GOOGLE_CLOUD_CREDENTAILS  = {"web":{
    "client_id": os.getenv("CLIENT_ID"),
    "project_id": os.getenv("PROJECT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_urlL": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "redirect_uris":redirect_uris
}}
print("Google cloud credentials:" ,GOOGLE_CLOUD_CREDENTAILS)
ALLOWED_HOSTS = [
    "*"
]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "app.backends.EmailBackend.EmailBackend",
]
# Application definition
SITE_ID = 2

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "app",
    "corsheaders",
    "djstripe",
    "django_q",
    "storages"
]
Q_CLUSTER = {
    'name': 'DjangoQCluster',
    'workers': 4,
    'recycle': 500,
    'timeout': 90,
    'orm':'default',
    'django_orm': 'default',
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

NICHES = ["custom", "fun_fact", "motivational", "life_tips", "philosophy", "jokes", "iq", "scary_story", "bedtime_story"]
ALLOWED_FREE_VOICES = ["alloy","echo","fable","onyx","nova","shimmer"]
ALLOWED_VOICES =  ALLOWED_FREE_VOICES + ["adam", "alic", "bill", "drew", "clyde", "paul", "domi", "dave", "fin", "sarah", "rachel"]
ALLOWED_FREE_ARTS = ["Default"]
ARTS = ["Comic book style", "Breathtaking anime-style", "Photo Realism style", "Disney toon style", "3D Minecraft style", "Default"]
PRICINGS = {
    "free": {
        "watermark_enabled": True,
        "credits_limits":1,
        "Price": 0,
        "processing_minutes_limits": 60,
        "uploaded_counts_limits": 1,
        "video_quality": "medium",
        "tokens_limits":10,
        "images_limits":5
    },
    "starter": {
        "credits_limits":25, # $14 
        "watermark_enabled": False,
        "Price": {"Monthly": 9.99, "Yearly": 96},
        "processing_minutes_limits": 1000,
        "uploaded_counts_limits": 100,
        "video_quality": "high",
        "tokens_limits":10,
        "images_limits":30


    },
    "pro": {
        "credits_limits":45, # $50 
        "watermark_enabled": False,
        "Price": {"Monthly": 19.99, "Yearly": 192},
        "processing_minutes_limits": 3000,
        "uploaded_counts_limits": 200,
        "video_quality": "high",
        "tokens_limits":10,
        "images_limits":40

    },
    "premuim":{
        "credits_limits":45, # $50 
        "watermark_enabled": False,
        "Price": {"Monthly": 19.99, "Yearly": 192},
        "processing_minutes_limits": 3000,
        "uploaded_counts_limits": 200,
        "video_quality": "high",
        "tokens_limits":10,
        "images_limits":40
    }
    ,
}

# Set the authentication classes

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'app': {  # Custom logger for your application
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]
ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases




DATABASES = {}

DATABASES["default"] = {
   "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.getenv("DB_PATH") + "/database.db",
}
#else:
#DATABASES ["default"] = {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#        "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT"),
#         "OPTIONS": {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#
#}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

CORS_ALLOW_HEADERS = [
    "Content-Type",
    "Authorization",
    "Access-Control-Allow-Origin",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# This ensures cookies are only sent over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Other security-related settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.titan.email"
EMAIL_HOST_ = "imap.titan.email"

EMAIL_PORT_SMTP = 587
EMAIL_PORT_IMAP = 993

EMAIL_HOST_USER = "admin@reelze.app"  # Your Gmail address
EMAIL_USE_SSL = True
# EMAIL_HOST_PASSWORD =  ssm.get_parameter(Name='EMAIL_HOST_PASSWORD', WithDecryption=True)['Parameter']['Value']
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "app/emails"  # This will create an 'emails' directory inside 'app'

# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    'https://reelze.app',
    'https://www.reelze.app',
    ]



    
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"




MUSICS =  [{'name': 'Hotline',
  'key': 'hotline',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/hotline.mp3'},
 {'name': 'Bladerunner 2049',
  'key': 'bladerunner-2049',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/bladerunner-2049.mp3'},
 {'name': 'Fallen',
  'key': 'fallen',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/fallen.mp3'},
 {'name': 'Constellations',
  'key': 'constellations',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/constellations.mp3'},
 {'name': 'Paris - Else',
  'key': 'paris---else',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/paris---else.mp3'},
 {'name': 'Another Love',
  'key': 'another-love',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/another-love.mp3'},
 {'name': 'Snowfall',
  'key': 'snowfall',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/snowfall.mp3'},
 {'name': 'Nas',
  'key': 'nas',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/nas.mp3'},
 {'name': "I'm Free",
  'key': 'im-free',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/im-free.mp3'},
 {'name': 'Once in Paris',
  'key': 'once-in-paris',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/once-in-paris.mp3'},
 {'name': 'Drops',
  'key': 'drops',
  'url': 'https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/drops.mp3'}]

SERVER_ENDPOINT_REDIRECT = f"{BACKEND_URL}/api/tiktok-callback"
TIKTOK_ACCESS_URL = "https://www.tiktok.com/v2/auth/authorize/"

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid']
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')