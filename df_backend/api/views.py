from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from . import models, serializers


class GetEntities(APIView):
    def get(self):
        """ GET will fetch a single, random character """

    def post(self):
        """ POST will allow multiple characters with options """


class RaceList(ListAPIView):
    queryset = models.EntityRace.objects.all()
    serializer_class = serializers.RaceSerializer


class ProfessionList(ListAPIView):
    queryset = models.EntityProfession.objects.all()
    serializer_class = serializers.ProfessionSerializer


class FactionList(ListAPIView):
    queryset = models.EntityFaction.objects.all()
    serializer_class = serializers.FactionSerializer


class EntityList(ListAPIView):
    serializer_class = serializers.EntitySerializer

    def get_queryset(self):
        return models.GameEntity.filter(game_map__game__player=self.request.user)


class NamePartViewSet(ModelViewSet):
    queryset = models.NamePart.objects.all()
    serializer_class = serializers.NamePartSerializer
    permission_classes = (IsAdminUser,)


class RaceViewSet(ModelViewSet):
    queryset = models.EntityRace.objects.all()
    serializer_class = serializers.RaceSerializer
    permission_classes = (IsAdminUser,)


class ProfessionViewSet(ModelViewSet):
    queryset = models.EntityProfession.objects.all()
    serializer_class = serializers.ProfessionSerializer
    permission_classes = (IsAdminUser,)


class FactionViewSet(ModelViewSet):
    queryset = models.EntityFaction.objects.all()
    serializer_class = serializers.FactionSerializer
    permission_classes = (IsAdminUser,)


class EntityViewSet(ModelViewSet):
    queryset = models.GameEntity.objects.all()
    serializer_class = serializers.EntitySerializer
    permission_classes = (IsAdminUser,)
