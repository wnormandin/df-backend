""" Resource generation scripts, api-specific miscellany """

import logging
import random
import requests
from collections import OrderedDict

from . import models, serializers
from .. import exc


logger = logging.getLogger(__name__)


class NameDescriptor:
    @classmethod
    def from_instance(cls, instance):
        return cls(**serializers.NamePartSerializer(instance).data)

    def __init__(self, paternal, maternal, prefix, suffix, **kwargs):
        self.paternal = paternal
        self.maternal = maternal
        self.prefix = prefix
        self.suffix = suffix

    def __bool__(self):
        return self.has_flags

    @property
    def core_flags(self):
        return self.paternal, self.maternal, self.prefix, self.suffix

    @property
    def has_flags(self):
        return any(self.core_flags)

    @property
    def value(self):
        parts = []
        if self.paternal:
            parts.append('pat')
        if self.maternal:
            parts.append('mat')
        if self.prefix:
            parts.append('pre')
        if self.suffix:
            parts.append('suf')

        if not parts:
            return
        return '[' + '|'.join(parts) + ']'


def register_user(username, password, email, first_name=None, last_name=None):
    """ Basic user registration, creates a game/game map by default """




def roll(d=0.5):
    return random.random() > (1-d)


def generate_multiple_names(count, genders=None, max_length=50, max_tries=100):
    results = []
    genderset = genders or ['male', 'female']
    for n in range(0, count):
        gender = random.choice(genderset)
        name_ = generate_name(gender=gender, max_length=max_length, max_tries=max_tries)
        if name_:
            results.append({'gender': gender, 'name': name_})
    return results


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


def generate_entity(gender, race, prof):
    if not isinstance(race, models.EntityRace):
        race = models.EntityRace.objects.get(name=race)
    if not isinstance(prof, models.EntityProfession):
        prof = models.EntityProfession.objects.get(name=prof)

    if prof not in race.allowed_professions():
        raise exc.InvalidProfessionSelection(f'{race} may not be {prof}')

    if gender not in ('male', 'female'):
        raise exc.InvalidGender(f'Unknown gender: {gender}')

    entity_name = generate_name(gender=gender)
