import logging
import logging.config

logger = logging.getLogger(__name__)

# load config from file 

# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

# or, for dictConfig

logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem

    'filename': 'infectionLog.log',
    'filemode': 'w',

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',    
            'class':'logging.StreamHandler',
        },  
        'toFile': {
            'filename': 'testLog.log',
            'mode':'w',
            'level':'INFO',
            'class':'logging.FileHandler',
        },
    },
    'loggers': {
        '': {                  
            'handlers': ['toFile', 'default'],
            'level': 'INFO',  
            'propagate': True  
        }
    }
})

logger.info('it works!')