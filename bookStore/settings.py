"""
Django settings for bookStore project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b-sx0!!4tfs68jl!1&xu6k19z!tll^c#oh947ex*bnlfe=eof@'

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
    'bookStoreApp',
    'rest_framework',
    'bookStoreAPI',
    'djmoney',
]

# Django-money custom deserializer

SERIALIZATION_MODULES = {"json": "djmoney.serializers"}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookStore.urls'

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

WSGI_APPLICATION = 'bookStore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

load_dotenv()

# local db
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_port = os.getenv("DB_PORT")

# Neon db
database_host_neon = os.getenv("PG_HOST")
database_name_neon = os.getenv("PG_DATABASE")
database_user_neon = os.getenv("PG_USER")
database_password_neon = os.getenv("PG_PASSWORD")
database_port_neon = os.getenv("PG_PORT")

# Render db
render_host = os.getenv("RD_HOST")
render_database = os.getenv("RD_DATABASE")
render_user = os.getenv("RD_USER")
render_password = os.getenv("RD_PASSWORD")
render_port = os.getenv("RD_PORT")

DATABASES = {
    # Neon

    # 'neon': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': database_name_neon,
    #     'USER': database_user_neon,
    #     'PASSWORD': database_password_neon,
    #     'HOST': database_host_neon,
    #     'PORT': database_port_neon,
    #     'OPTIONS': {
    #         'sslmode': 'require',
    #     },
    # },
    # 'local': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'book_store',
    #     'USER': database_user,
    #     'PASSWORD': database_password,
    #     'HOST': 'localhost',
    #     'PORT': database_port
    # },

    # Render - seems load quiker than Neon
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': render_database,
        'USER': render_user,
        'PASSWORD': render_password,
        'HOST': render_host,
        'PORT': render_port
    }
}

AUTH_USER_MODEL = 'auth.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Addis_Ababa'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
