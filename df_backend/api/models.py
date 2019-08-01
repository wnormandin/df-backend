from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import logging
import random

from ..utils.constants import GENDER_CHOICES

logger = logging.getLogger(__name__)


class NamePart(models.Model):
    value = models.CharField(max_length=15)
    paternal = models.BooleanField(default=False)
    maternal = models.BooleanField(default=False)
    prefix = models.BooleanField(default=False)
    suffix = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='neutral')

    @classmethod
    def get_part(cls, target=None, gender='neutral'):
        filter_kwargs = dict(paternal=False, maternal=False, prefix=False, suffix=False)
        filter_kwargs['gender__in'] = {gender, 'neutral'}

        if target is not None:
            filter_kwargs[target] = True
        if target == 'paternal':
            filter_kwargs.pop('maternal')
        elif target == 'maternal':
            filter_kwargs.pop('paternal')

        targets = cls.objects.filter(**filter_kwargs).all()
        return random.choice(list(targets)) if targets else None


class Game(models.Model):
    player = models.ForeignKey(User, models.DO_NOTHING, related_name='games')
    created_at = models.DateTimeField(default=datetime.utcnow)


class GameMap(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    created_at = models.DateTimeField(default=datetime.utcnow)


# Create your models here.
class GameEntity(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    alive = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='neutral')

    profession = models.ForeignKey('EntityProfession', models.DO_NOTHING)
    race = models.ForeignKey('EntityRace', models.DO_NOTHING)
    stats = models.ForeignKey('EntityStats', models.DO_NOTHING)
    location = models.ForeignKey('EntityLocation', models.DO_NOTHING)
    game_map = models.ForeignKey(GameMap, models.DO_NOTHING)

    @classmethod
    def get_random(cls):
        """ Returns a randomly generated entity without restrictions """

        entity = cls()

    def get_faction_scores(self):
        output = {}
        for rel in EntityFaction.objects.filter(entity=self):
            score = FactionScore.objects.get(entity=self, faction=rel.faction)
            output[rel.faction.name] = score.value
        return output

    def initialize_factions(self):
        for faction in EntityFaction.objects.all():
            FactionScore.objects.create(entity=self, faction=faction)

    def initialize_stats(self):
        if not self.stats:
            self.stats = EntityStats.objects.create()

    def select_race(self, race):
        self.race = race
        self.stats.apply_modifiers(race.stats)
        self.save()

    def select_profession(self, profession):
        assert self.race is not None
        assert self.race in profession.allowed_races

        self.profession = profession
        self.stats.apply_modifiers(profession.stats)
        self.save()

    def set_position(self, x, y, z):
        self.location.x = x
        self.location.y = y
        self.location.z = z


class EntityLocation(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)

    def position(self):
        return self.x, self.y, self.z


class ProfessionRace(models.Model):
    profession = models.ForeignKey('EntityProfession', models.DO_NOTHING,
                                   related_name='races')
    race = models.ForeignKey('EntityRace', models.DO_NOTHING)

    class Meta:
        unique_together = [['profession', 'race']]


class EntityProfession(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    stats = models.ForeignKey('StatModifiers', models.DO_NOTHING)

    def allowed_races(self):
        return [rel.race for rel in self.races.get()]


class EntityRace(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    stats = models.ForeignKey('StatModifiers', models.DO_NOTHING)


class FactionScore(models.Model):
    entity = models.ForeignKey(GameEntity, models.DO_NOTHING)
    faction = models.ForeignKey('EntityFaction', models.DO_NOTHING)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = [['entity', 'faction']]


class EntityFaction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)


class EntityStats(models.Model):
    food = models.IntegerField(default=100)
    drink = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)

    # Core
    toughness = models.IntegerField(default=1)
    agility = models.IntegerField(default=1)
    dexterity = models.IntegerField(default=1)
    intelligence = models.IntegerField(default=1)
    wisdom = models.IntegerField(default=1)

    # Social
    charm = models.IntegerField(default=1)
    persuasion = models.IntegerField(default=1)
    introversion = models.IntegerField(default=1)
    stability = models.IntegerField(default=1)
    friendliness = models.IntegerField(default=1)

    # Resists
    elements = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)
    magic = models.IntegerField(default=0)
    hunger = models.IntegerField(default=0)
    thirst = models.IntegerField(default=0)
    exhaustion = models.IntegerField(default=0)

    # Mental attributes
    stress = models.IntegerField(default=100)
    happiness = models.IntegerField(default=100)
    addiction = models.IntegerField(default=100)

    def apply_modifiers(self, modifiers):

        for key, value in modifiers.serialize().items():
            if key in ('name', 'description'):
                continue

            logger.debug(f'Changing stat {key} by {value}')
            setattr(self, key, getattr(self, key) + value)
            logger.debug(f'New value: {getattr(self, key)}')

        self.save()

    def serialize(self):
        from . import serializers
        return serializers.StatSerializer(self).data


class StatModifiers(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    food = models.IntegerField(default=0)
    drink = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    # Core
    toughness = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    dexterity = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)

    # Social
    charm = models.IntegerField(default=0)
    persuasion = models.IntegerField(default=0)
    introversion = models.IntegerField(default=0)
    stability = models.IntegerField(default=0)
    friendliness = models.IntegerField(default=0)

    # Resists
    elements = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)
    magic = models.IntegerField(default=0)
    hunger = models.IntegerField(default=0)
    thirst = models.IntegerField(default=0)
    exhaustion = models.IntegerField(default=0)

    # Mental attributes
    stress = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)
    addiction = models.IntegerField(default=0)

    def serialize(self):
        from . import serializers
        return serializers.StatSerializer(self).data
