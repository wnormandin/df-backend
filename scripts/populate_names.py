from df_backend.api.resources import load_names_from_url
from df_backend.api import models
import logging


logger = logging.getLogger('df_backend')


definitions = {
    'https://raw.githubusercontent.com/arineng/arincli/master/lib/female-first-names.txt': {
        'gender': 'female'
    },
    'https://raw.githubusercontent.com/arineng/arincli/master/lib/male-first-names.txt': {
        'gender': 'male'
    },
    'https://raw.githubusercontent.com/arineng/arincli/master/lib/last-names.txt': {
        'paternal': True, 'maternal': True
    }
}

prefixes = {
    'Dr': {'prefix': True},
    'Hon': {'prefix': True},
    'Mr': {'gender': 'male', 'prefix': True},
    'Ms': {'gender': 'female', 'prefix': True},
    'Mrs': {'gender': 'female', 'prefix': True},
}

suffixes = {
    'II': {'suffix': True},
    'III': {'suffix': True},
    'Jr': {'suffix': True},
    'Sr': {'suffix': True},
    'Esq': {'suffix': True},
    'PhD': {'suffix': True},
}

for key, kwargs in {**prefixes, **suffixes}.items():
    models.NamePart.objects.create(value=key, **kwargs)
    logger.debug(f'Inserted {key} ({kwargs})')


for url, kwargs in definitions.items():
    logger.debug(f'Processing:\n{url}\n{kwargs}')
    logger.debug(load_names_from_url(url, **kwargs))
