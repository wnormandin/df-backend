from . import MarkModelDeletedViewSet
from .. import models, serializers


class NamePartViewSet(MarkModelDeletedViewSet):
    queryset = models.NamePart.objects.all()
    serializer_class = serializers.NamePartSerializer


class RaceViewSet(MarkModelDeletedViewSet):
    queryset = models.EntityRace.objects.all()
    serializer_class = serializers.RaceSerializer


class ProfessionViewSet(MarkModelDeletedViewSet):
    queryset = models.EntityProfession.objects.all()
    serializer_class = serializers.ProfessionSerializer


class FactionViewSet(MarkModelDeletedViewSet):
    queryset = models.EntityFaction.objects.all()
    serializer_class = serializers.FactionSerializer


class EntityViewSet(MarkModelDeletedViewSet):
    queryset = models.GameEntity.objects.all()
    serializer_class = serializers.EntitySerializer


__all__ = ['NamePartViewSet', 'RaceViewSet', 'ProfessionViewSet', 'FactionViewSet', 'EntityViewSet']