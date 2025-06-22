# config/settings.py (VERSÃO FINAL SEGUINDO A DOCUMENTAÇÃO)

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-local-key-for-dev-only')
DEBUG = not (os.getenv('USE_S3') == 'TRUE')
ALLOWED_HOSTS = []

# Application definition e Middleware (mantenha igual)
INSTALLED_APPS = [
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes',
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig', 
    'users.apps.UsersConfig', 
    'catalog.apps.CatalogConfig',
    'submission.apps.SubmissionConfig',
    'comments.apps.CommentsConfig',
    'storages',
    'mptt', 
    'ckeditor', 
    'ckeditor_uploader',
    'django.contrib.sites',
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [ #... Mantenha sua config de TEMPLATES
    {'BACKEND': 
     'django.template.backends.django.DjangoTemplates',
     'DIRS': [os.path.join(BASE_DIR, 'templates')],
     'APP_DIRS': True,
     'OPTIONS': {'context_processors': ['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',],},
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', conn_max_age=600)}

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]

# config/settings.py
AUTHENTICATION_BACKENDS = [
    # Necessário para logar no admin com username
    'django.contrib.auth.backends.ModelBackend',

    # Lógicas de autenticação do allauth, como login por e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1 # allauth usa o framework de sites do Django


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- LÓGICA FINAL PARA ARQUIVOS DE MÍDIA SEGUINDO A DOCUMENTAÇÃO ---
USE_S3 = os.getenv('USE_S3') == 'TRUE'
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = 'media'
    CKEDITOR_STORAGE_BACKEND = 'config.storages.S3MediaStorage'
    
else:
    # Configurações para desenvolvimento local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    CKEDITOR_STORAGE_BACKEND = 'django.core.files.storage.DefaultStorage'

# Outras configs
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_STORAGE_BACKEND = "django.core.files.storage.DefaultStorage"

# --- CONFIGURAÇÕES DO DJANGO-ALLAUTH ---
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True # Ou False, se você preferir login só por e-mail
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # Permite login com user ou e-mail
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # Força a verificação do e-mail

LOGIN_REDIRECT_URL = 'dashboard' # Para onde vai após o login
LOGOUT_REDIRECT_URL = 'home' # Para onde vai após o logout

# Para desenvolvimento, os e-mails de verificação serão impressos no console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ALLOWED_HOSTS
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if not USE_S3:
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('localhost')
