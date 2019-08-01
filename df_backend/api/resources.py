""" Resource generation scripts, api-specific miscellany """

import logging
import random
import requests
from collections import OrderedDict

from ..utils import constants
from . import models, serializers


logger = logging.getLogger(__name__)


def roll(d=0.5):
    return random.random() > (1-d)


def generate_name(gender, max_length=50, max_tries=100):
    odds = OrderedDict()
    odds['prefix'] = 0.1
    odds[None] = 1
    odds['middle'] = 0.25
    odds['paternal'] = 1
    odds['maternal'] = 0.25
    odds['suffix'] = 0.1

    get = models.NamePart.get_part
    attempt = 0

    while attempt < max_tries:
        name = ''
        for target, difficulty in odds.items():
            if roll(d=difficulty):
                comma = ', ' if target == 'suffix' else ''
                hyphen = '-' if target == 'maternal' and roll() else ' '
                part = get(target=None if target == 'middle' else target,
                           gender=gender)

                if part is None:
                    return False

                name += f'{comma or hyphen}{part.value}'

        if len(name) > max_length:
            attempt += 1
            continue
        else:
            return name.strip()


def load_names_from_url(url, max_count=2000, **kwargs):
    assert url.endswith('.txt')
    data = requests.get(url).content.decode().split()

    if 'gender' not in kwargs:
        kwargs['gender'] = 'neutral'

    count = 0
    for item in data:
        models.NamePart.objects.create(value=item.title(), **kwargs)
        logger.debug(f'Stored name {item.title()}')
        count += 1

        if count > max_count:
            break

    return count


def generate_entity():
    pass
