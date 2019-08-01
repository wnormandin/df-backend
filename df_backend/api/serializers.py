from rest_framework import serializers
from django.contrib.auth.models import User

from . import models


class StatSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=50)
    description = serializers.CharField(required=False, max_length=1000)

    food = serializers.IntegerField()
    drink = serializers.IntegerField()
    stamina = serializers.IntegerField()

    # Core
    toughness = serializers.IntegerField()
    agility = serializers.IntegerField()
    dexterity = serializers.IntegerField()
    intelligence = serializers.IntegerField()
    wisdom = serializers.IntegerField()

    # Social
    charm = serializers.IntegerField()
    persuasion = serializers.IntegerField()
    introversion = serializers.IntegerField()
    stability = serializers.IntegerField()
    friendliness = serializers.IntegerField()

    # Resists
    elements = serializers.IntegerField()
    physical = serializers.IntegerField()
    magic = serializers.IntegerField()
    hunger = serializers.IntegerField()
    thirst = serializers.IntegerField()
    exhaustion = serializers.IntegerField()

    # Mental attributes
    stress = serializers.IntegerField()
    happiness = serializers.IntegerField()
    addiction = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class NamePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NamePart
        fields = '__all__'


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntityRace
        fields = '__all__'


class ProfessionSerializer(serializers.ModelSerializer):
    allowed_races = RaceSerializer(many=True)

    class Meta:
        model = models.EntityProfession
        fields = '__all__'


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntityFaction
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    player = UserSerializer()

    class Meta:
        model = models.Game
        fields = '__all__'


class GameMapSerializer(serializers.ModelSerializer):
    game = GameSerializer()

    class Meta:
        model = models.GameMap
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    value = serializers.ListField(serializers.IntegerField(), source='position',
                                  max_length=3, min_length=3)

    class Meta:
        from . import models
        model = models.EntityLocation
        exclude = ['x', 'y', 'z', 'id']


class EntitySerializer(serializers.Serializer):
    stats = StatSerializer(required=False)
    race = RaceSerializer(required=False)
    profession = ProfessionSerializer(required=False)
    factions = serializers.DictField(source='get_faction_scores', required=False)
    location = PositionSerializer(required=False)
    game_map = GameMapSerializer()

    class Meta:
        model = models.GameEntity
        fields = ['id', 'name', 'level', 'alive', 'active',
                  'profession', 'race', 'stats', 'location', 'game_map']
