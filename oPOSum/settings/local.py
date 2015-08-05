import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = '/oposm/oPOSum/oposum/static/imgs/'

MEDIA_URL = '/media/'

STATIC_ROOT = '/oposm/oPOSum/oposum/static/'

STATIT_URL = '/static/'
