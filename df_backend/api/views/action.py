
from rest_framework import status, response, views

from .. import serializers, resources


class GetEntities(views.APIView):
    def get(self, request):
        """ GET will fetch a single, random character """

        entity = resources.generate_entity('male', 'TestHuman', 'TestWarrior', created_by=request.user)
        return response.Response(serializers.EntitySerializer(entity).data)

    def post(self, request):
        """ POST will allow multiple characters with options """


class RandomNameGeneration(views.APIView):
    def get(self, request, count=None, format=None):
        """ Fetch {count} random names with randomized genders """

        names = resources.generate_multiple_names(int(count or 1))
        response_code = status.HTTP_202_ACCEPTED if names else status.HTTP_404_NOT_FOUND

        return response.Response({'result': names}, status=response_code)

    def post(self, request, count=None, format=None):
        """ Fetch {count} random names, may specify "genders" in the body """

        serializer = serializers.RandomNameRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        count = int(count or serializer.data.get('count'))
        genders = serializer.data.get('genders')
        names = resources.generate_multiple_names(count, genders=genders)
        response_code = status.HTTP_202_ACCEPTED if names else status.HTTP_404_NOT_FOUND

        return response.Response({'result': names}, status=response_code)


class RegisterUser(views.APIView):
    def post(self, request, format=None):
        """ Register a new user account """

        serializer = serializers.NewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(
            resources.register_user(**serializer.data),
            status=status.HTTP_201_CREATED)


__all__ = ['GetEntities', 'RandomNameGeneration', 'RegisterUser']
