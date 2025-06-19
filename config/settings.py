import os
from pathlib import Path
import dj_database_url # Importa o novo pacote

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega a SECRET_KEY do ambiente. Se não encontrar, usa uma chave insegura (só para emergências locais).
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-^cuf)nz_*eiy&&4t16$-ea0p06w388)^bqvn0n*w)78=7ox=%z')

# O modo DEBUG será 'True' apenas se a variável de ambiente DEBUG for 'TRUE'. No Render, ela é 'FALSE'.
DEBUG = os.getenv('DEBUG') == 'TRUE'

# Configuração de ALLOWED_HOSTS
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Adiciona o localhost para desenvolvimento apenas se não estivermos em produção
if not os.getenv('USE_S3'):
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('localhost')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Nossos apps
    'pages.apps.PagesConfig', # Adicione esta linha
    'users.apps.UsersConfig',
    'catalog.apps.CatalogConfig',
    'submission.apps.SubmissionConfig',
    # Apps de terceiros
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
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
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        # Fallback para sqlite se DATABASE_URL não estiver definida
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600 # Mantém as conexões abertas por 600s
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Campo_Grande' # Horário local
USE_I18N = True
USE_TZ = True

# --- Arquivos Estáticos (CSS, JS do Admin, etc.) ---
# Servidos pelo WhiteNoise em produção
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Arquivos de Mídia (Uploads de usuários) ---
# Servidos pelo S3 em produção
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Apenas em produção, configure o S3 para os uploads (mídia)
if os.getenv('USE_S3') == 'TRUE':
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'sa-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    # Define o S3 como o local para ARQUIVOS DE MÍDIA
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
    # A URL de mídia aponta para o S3
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'

# Configurações do CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_STORAGE_BACKEND = "django.core.files.storage.DefaultStorage"