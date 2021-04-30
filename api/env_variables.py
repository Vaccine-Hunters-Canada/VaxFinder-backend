import os
from loguru import logger
from api import logging_config

logging_config.make_logger()

def check_and_make() -> None:
    required_env_vars = [
            'DATABASE_URL',
        ]

    default_env_vars = {
        'DATABASE_URL': '',
    }
    
    if os.environ.get('ENV') is None:
         os.environ['ENV'] = 'development'

    missing_env = False
    for env in required_env_vars:
        if os.environ.get(env) is None:
            logger.warning(f'{env} not in environment variables')
            missing_env = True

            if os.environ['ENV'] == 'development':
                os.environ[env] = default_env_vars[env]
    
    if os.environ['ENV'] == 'production' and missing_env:
        raise KeyError('Missing environment variables')