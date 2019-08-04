from . import ModelListView
from .. import models, serializers


class LanguagesList(ModelListView):
    queryset = models.NameLanguage.objects.all()
    serializer_class = serializers.NameLanguageSerializer


class NameDomainList(ModelListView):
    queryset = models.NameDomain.objects.all()
    serializer_class = serializers.NameDomainSerializer


class NameEraList(ModelListView):
    queryset = models.NameEra.objects.all()
    serializer_class = serializers.NameEraSerializer


class RaceList(ModelListView):
    queryset = models.EntityRace.objects.all()
    serializer_class = serializers.RaceSerializer


class ProfessionList(ModelListView):
    queryset = models.EntityProfession.objects.all()
    serializer_class = serializers.ProfessionSerializer


class FactionList(ModelListView):
    queryset = models.EntityFaction.objects.all()
    serializer_class = serializers.FactionSerializer


class EntityList(ModelListView):
    serializer_class = serializers.EntitySerializer

    def get_queryset(self):
        return models.GameEntity.objects.filter(game_map__game__player=self.request.user)


__all__ = ['LanguagesList', 'NameDomainList', 'NameEraList', 'RaceList', 'ProfessionList',
           'FactionList', 'EntityList']
