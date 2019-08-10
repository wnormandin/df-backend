""" Resource generation scripts, api-specific miscellany """

import logging
import random
import requests
from collections import OrderedDict
from django.contrib.auth.models import User, Group

from . import models, serializers
from .. import exc, utils


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

    # Create our user and add them to the player group
    user = User.objects.create_user(username, email=email, password=password,
                                    first_name=first_name, last_name=last_name)
    user.groups.add(get_player_group())


def roll(d=0.5):
    return random.random() > (1-d)


def get_user_by_username(username):
    return User.objects.get_by_natural_key(username)


def get_group_by_name(groupname):
    return Group.objects.filter(name=groupname).first()


def get_player_group():
    return get_group_by_name(utils.constants.DF_PLAYER_GROUP)


def get_system_user():
    return get_user_by_username(utils.constants.DF_SYSTEM_USER)


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


def generate_entity(gender, race, prof, created_by=None, game_map=None):
    if not isinstance(race, models.EntityRace):
        race = models.EntityRace.objects.get(name=race)
    if not isinstance(prof, models.EntityProfession):
        prof = models.EntityProfession.objects.get(name=prof)

    if prof not in race.allowed_professions():
        raise exc.InvalidProfessionSelection(f'{race} may not be {prof}')

    if gender not in ('male', 'female'):
        raise exc.InvalidGender(f'Unknown gender: {gender}')

    entity_name = generate_name(gender=gender)
    return models.GameEntity.generate_entity(entity_name, gender=gender, race=race, profession=prof,
                                             created_by=created_by or get_system_user(), game_map=game_map)


def server_log(message, created_by=None, **kwargs):
    return models.ServerLog.objects.create(message=message, created_by=created_by, **kwargs).id
