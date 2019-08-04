from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import logging
import random

from ..utils.constants import GENDER_CHOICES

logger = logging.getLogger(__name__)


class CreationTrackingModel(models.Model):
    """ Model base including mechanism to track creation time / user for each record """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def mark_deleted(self):
        self.deleted = True


class NameDomain(CreationTrackingModel):
    """ reality, lotr, general fantasy, etc """

    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name.title()


class NameLanguage(CreationTrackingModel):
    """ Etymological name language """

    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name.title()


class NameEra(CreationTrackingModel):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=1000)

    domain = models.ForeignKey(NameDomain, models.CASCADE, related_name='eras', null=True)

    def __str__(self):
        return self.name.title()


class NamePart(CreationTrackingModel):
    value = models.CharField(max_length=15)

    paternal = models.BooleanField(default=False)
    maternal = models.BooleanField(default=False)
    prefix = models.BooleanField(default=False)
    suffix = models.BooleanField(default=False)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='neutral')
    era = models.ForeignKey(NameEra, models.CASCADE, related_name='names', null=True)
    language = models.ForeignKey(NameLanguage, models.CASCADE, related_name='names', null=True)

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

    def __str__(self):
        return f'{self.value} ({self.gender} {self.desc.value + " " if self.desc else ""}name)'

    @property
    def desc(self):
        from .resources import NameDescriptor
        return NameDescriptor.from_instance(self)


class Game(CreationTrackingModel):
    player = models.ForeignKey(User, models.CASCADE, related_name='games')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.player} game {self.id}'


class GameMap(CreationTrackingModel):
    game = models.ForeignKey(Game, models.CASCADE)
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.game} map {self.id}'


class GameEntity(CreationTrackingModel):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    alive = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='neutral')

    profession = models.ForeignKey('EntityProfession', models.CASCADE)
    race = models.ForeignKey('EntityRace', models.CASCADE)
    stats = models.ForeignKey('EntityStats', models.CASCADE)
    location = models.ForeignKey('EntityLocation', models.CASCADE)
    game_map = models.ForeignKey(GameMap, models.CASCADE)

    @classmethod
    def generate_entity(cls, name, gender, race, profession):
        entity = cls.objects.create(name=name, gender=gender)

    def __str__(self):
        return f'{self.name.title()} (lvl {self.level} {self.race} {self.profession})'

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


class EntityLocation(CreationTrackingModel):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)

    def position(self):
        return self.x, self.y, self.z

    def __str__(self):
        return f'({self.x},{self.y},{self.z})'


class ProfessionRace(CreationTrackingModel):
    profession = models.ForeignKey('EntityProfession', models.CASCADE,
                                   related_name='races')
    race = models.ForeignKey('EntityRace', models.CASCADE, related_name='professions')

    class Meta:
        unique_together = [['profession', 'race']]


class EntityProfession(CreationTrackingModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    stats = models.ForeignKey('StatModifiers', models.CASCADE)

    def __str__(self):
        return self.name.title()

    def allowed_races(self):
        return [rel.race for rel in self.races.get()]


class EntityRace(CreationTrackingModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    stats = models.ForeignKey('StatModifiers', models.CASCADE)

    def __str__(self):
        return self.name.title()

    def allowed_professions(self):
        return [rel.profession for rel in self.professions.get()]


class FactionScore(CreationTrackingModel):
    entity = models.ForeignKey(GameEntity, models.CASCADE)
    faction = models.ForeignKey('EntityFaction', models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = [['entity', 'faction']]


class EntityFaction(CreationTrackingModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name.title()


class EntityStats(CreationTrackingModel):
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


class StatModifiers(CreationTrackingModel):
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

    def __str__(self):
        return self.name.title()


class LogType(CreationTrackingModel):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)


class ServerLog(CreationTrackingModel):
    message = models.CharField(max_length=1000)

    # Potential relationships
    player = models.ForeignKey(User, models.SET_NULL, null=True, related_name='logs')
    game = models.ForeignKey(Game, models.SET_NULL, null=True)
    game_map = models.ForeignKey(GameMap, models.SET_NULL, null=True)
    entity = models.ForeignKey(GameEntity, models.SET_NULL, null=True)
    race = models.ForeignKey(EntityRace, models.SET_NULL, null=True)
    profession = models.ForeignKey(EntityProfession, models.SET_NULL, null=True)

    # Log Message Metadata
    logtype = models.ForeignKey(LogType, models.SET_NULL, related_name='logs', null=True)
    context = models.CharField(max_length=1000)
    remote_addr = models.GenericIPAddressField(null=True)
    err_host = models.GenericIPAddressField(null=True)
