# config/settings.py (VERSÃO FINAL E REESTRUTURADA)

import os
from pathlib import Path
import dj_database_url
import logging

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Chaves e Configurações de Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-local-key-for-dev')
DEBUG = os.getenv('DEBUG') == 'TRUE'
ALLOWED_HOSTS = []

# --- DEFINIÇÃO INCONDICIONAL DOS STORAGES ---
# Dizemos ao Django DESDE O INÍCIO quais classes usar.
# A lógica de qual storage usar (local vs S3) estará dentro da própria classe.
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Nossos apps
    'pages.apps.PagesConfig',
    'users.apps.UsersConfig',
    'catalog.apps.CatalogConfig',
    'submission.apps.SubmissionConfig',
    # Apps de terceiros
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Middleware do WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [ #... (pode manter sua configuração de TEMPLATES igual)
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', conn_max_age=600)}

# Password validation, etc... (mantenha o resto das suas configs)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Campo_Grande'
USE_I18N = True
USE_TZ = True

# --- CONFIGURAÇÃO DOS ARQUIVOS ESTÁTICOS E DE MÍDIA ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- CONFIGURAÇÃO DAS VARIÁVEIS DO S3 ---
# Estas variáveis só serão usadas pela classe MediaStorage se USE_S3 for TRUE
USE_S3 = os.getenv('USE_S3')
if USE_S3:
    # Credenciais
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Configuração do Bucket
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    # Comportamento dos Arquivos
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read' # Para que os arquivos sejam publicamente acessíveis

    # Backend de Armazenamento
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

    # URL para acessar os arquivos (formato padrão)
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

# Outras configs
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_STORAGE_BACKEND = "django.core.files.storage.DefaultStorage"

# Configuração de ALLOWED_HOSTS (movido para o final para garantir que as variáveis sejam lidas)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if not USE_S3: # Adiciona localhost em desenvolvimento
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('localhost')

# Teste de logging (pode remover depois)
logging.warning(">>> NOVA CONFIGURACAO DE SETTINGS CARREGADA <<<")