from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser

from . import models, serializers, resources


class GetEntities(APIView):
    def get(self):
        """ GET will fetch a single, random character """

    def post(self):
        """ POST will allow multiple characters with options """


class RandomNameGeneration(APIView):
    def get(self, request, count=None, format=None):
        """ Fetch {count} random names with randomized genders """

        names = resources.generate_multiple_names(int(count or 1))
        response_code = status.HTTP_202_ACCEPTED if names else status.HTTP_404_NOT_FOUND

        return Response({'result': names}, status=response_code)

    def post(self, request, count=None, format=None):
        """ Fetch {count} random names, may specify "genders" in the body """

        serializer = serializers.RandomNameRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        count = int(count or serializer.data.get('count'))
        genders = serializer.data.get('genders')
        names = resources.generate_multiple_names(count, genders=genders)
        response_code = status.HTTP_202_ACCEPTED if names else status.HTTP_404_NOT_FOUND

        return Response({'result': names}, status=response_code)


class RegisterUser(APIView):
    def post(self, request, format=None):
        """ Register a new user account """

        serializer = serializers.NewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(resources.register_user(**serializer.data), status=status.HTTP_201_CREATED)


class LanguagesList(ListAPIView):
    queryset = models.NameLanguage.objects.all()
    serializer_class = serializers.NameLanguageSerializer


class NameDomainList(ListAPIView):
    queryset = models.NameDomain.objects.all()
    serializer_class = serializers.NameDomainSerializer


class NameEraList(ListAPIView):
    queryset = models.NameEra.objects.all()
    serializer_class = serializers.NameEraSerializer


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
        return models.GameEntity.objects.filter(game_map__game__player=self.request.user)


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
