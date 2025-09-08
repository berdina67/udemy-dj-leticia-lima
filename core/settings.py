# importar a biblioteca
import os
import sys
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

STATIC_DIR=os.path.join(BASE_DIR,'static') 


# Adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env")) 

# Diz para Projeto Django aonde estão nossos aplicativos
APPS_DIR = str(os.path.join(BASE_DIR,'apps')) # Dentro da pasta apps na raiz do projeto
sys.path.insert(0, APPS_DIR)

# Chamar as variaveis assim

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [
    'localhost', 
	'127.0.0.1', 
]

# Application definition 
DJANGO_APPS = [ # Aplicativos padrão do projeto django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [ # são as Lib/app que instalamos no projeto
    #... # update 11/03/2024 - removido esses ...
    "corsheaders",
]

PROJECT_APPS = [ # são os apps que criamos no projeto 
        'apps.base', # update 11/03/2024
        'apps.pages',
]

# INSTALLED_APPS é a variavel que django entende para fazer a leitura \
# dos aplicativos então verifica a nomencratura.
INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'requestlogs.middleware.RequestLogsMiddleware', #LOGS
]

# CORS Config
CORS_ALLOW_HEADERS = list(default_headers) + [
	'X-Register',
]

CORS_ORIGIN_ALLOW_ALL = True  
# CORS_ORIGIN_ALLOW_ALL como True, o que permite que qualquer site acesse seus recursos.
# Defina como False e adicione o site no CORS_ORIGIN_WHITELIST onde somente o site da lista acesse os seus recursos.

CORS_ALLOW_CREDENTIALS = False 

CORS_ORIGIN_WHITELIST = ['http://meusite.com',] # Lista. 

ROOT_URLCONF = 'core.urls'

if not DEBUG:
	SECURE_SSL_REDIRECT = True
	ADMINS = [(os.getenv('SUPER_USER'), os.getenv('EMAIL'))]
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True 

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
				
				#apps.base.context_processors.context_social_media, # update 08/09/2025
				'base.context_processors.context_social',
            ]
        },
    },
]

#WSGI_APPLICATION = 'secretaria.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases



# Banco de Dados.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, os.getenv('NAME_DB'))
            #'USER':os.getenv('USER_DB')
            #'PASSWORD': os.getenv('PASSWORD_DB')
            #'HOST':os.getenv('HOST_DB')
            #'PORT':os.getenv('PORT_DB') 
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/ 
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/' 

# STATICFILES_DIRS = [ # talvez em Produção podesse usar assim.
#     BASE_DIR / 'static',
# ]

MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

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

REST_FRAMEWORK={ 
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}

# Configuração padrão de Logs 
LOGGING = { # update 03/11/2024 
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'info.log',
            'when': 'midnight',  # Rotaciona a cada meia-noite
            'backupCount': 7,  # Mantém logs dos últimos 7 dias
            'formatter': 'verbose',  # Configuração de formatação
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
}

REQUESTLOGS = {
    'SECRETS': ['password', 'token'],
    'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
}

# Configuração de E-mail
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 
EMAIL_PORT = os.getenv('EMAIL_PORT') 
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') 
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
