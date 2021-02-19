import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'therapists',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
INSTALLED_APPS = [

    'therapist_profile',
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hho*9ou1_(t^&k(e5r=fmak!wq@-z@m&dti(o@3^=duv5*cj3b'
