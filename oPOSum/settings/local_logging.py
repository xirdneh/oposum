import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters':{
        'verbose':{
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
        },
        'simple':{
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers':{
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'oposm_pos_error':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': PROJECT_DIR + '/../logs/oposm.debug.log',
            'when': 'D',
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'backupCount': 0
        },
        'oposm_pos_debug':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': PROJECT_DIR + '/../logs/oposm.debug.log',
            'when': 'D',
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'backupCount': 0
        },
    },
    'loggers':{
        'django.request':{
            'handlers':['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'sales':{
            'handlers':['oposm_pos_error'],
            'level':'DEBUG',
            'propagate': True
        },
        'oPOSum':{
            'handlers':['oposm_pos_debug'],
            'level':'DEBUG',
            'propagate':True
        }
    }
}

