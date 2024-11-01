from pathlib import Path
import os
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kvbc9rbs4+#!p*zt0^7&ujkd4$0zvj$1)r5$g1os%hqhinre2-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Detectează automat adresa IP locală și adaugă-o la ALLOWED_HOSTS
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# ALLOWED_HOSTS configurat pentru a permite toate IP-urile locale și wildcard
ALLOWED_HOSTS = ['localhost', '127.0.0.1', local_ip, '*']

# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    

    # Custom apps
    'shortcuts.chrome',
    'shortcuts.file_explorer',
    'shortcuts.microsoft_excel',
    'shortcuts.microsoft_teams',
    'shortcuts.microsoft_word',
    'shortcuts.pdf',
    'shortcuts.powerpoint',
    'shortcuts.whatsapp',
    'shortcuts.skype',
    'shortcuts.keyboard_mouse',

    # Third-party apps
    'corsheaders',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'shortcuts.middleware.AppendSlashMiddleware',
]

ROOT_URLCONF = 'my_project.urls'

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

WSGI_APPLICATION = 'my_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
#STATICFILES_DIRS = [BASE_DIR / "static"]  # Pentru fișierele statice din proiect
STATIC_ROOT = BASE_DIR / "staticfiles"  # Directorul unde vor fi colectate toate fișierele statice

STATIC_URL = '/static/'  # Aceasta definește URL-ul fișierelor statice.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'shortcuts', 'static')]  # Definește calea completă către directorul static.




# Media files (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Directorul pentru fișierele media

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Adresa frontend-ului React
]

# Security settings for production (adjust as necessary)
# SECURE_SSL_REDIRECT = True  # Uncomment this line for SSL redirection in production
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'

# Logging configuration (optional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Adaugă următoarele setări
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']



SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Sesiuni stocate în baza de date
SESSION_COOKIE_SECURE = False  # False în mediul local
CSRF_COOKIE_SECURE = False  # False în mediul local


MSAL_CONFIG = {
    "client_id": "51624ba1-4a00-43c7-b5f1-2500ac4d5591",
    "client_secret": "2AC8Q~LUAxEBo5YFO~PL5s9hnpX6lmGkvVQEaa2a",
    "authority": "https://login.microsoftonline.com/common",
    "redirect_uri": "http://localhost:3000/shortcuts/teams",
    "scope": [
        "User.Read", 
        "Contacts.Read",
        #"Calls.AccessMedia.All", 
        #"Calls.Initiate.All", 
        #"Calls.InitiateGroupCall.All", 
        #"Calls.AccessMedia.All", 
       
    ],
    "post_logout_redirect_uri": "http://localhost:8000/shortcuts/teams/",
}


