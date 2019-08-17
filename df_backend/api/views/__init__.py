from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from ..serializers import UserSerializer
from df_backend import __version__ as api_version


class UserLogin(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token})


class ModelListView(ListAPIView):
    """ APIView base for ListViews to ensure we are applying DjangoModelPermissions """
    permission_classes = (DjangoModelPermissions,)


class MarkModelDeletedViewSet(ModelViewSet):
    """
    Viewset which prevents items from actually being deleted from the DB
    Instead, a `deleted` flag is set
    """

    permission_classes = (DjangoModelPermissions,)

    def perform_destroy(self, instance):
        instance.mark_deleted()
        instance.save()


class HeartBeatView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        userdata = UserSerializer(request.user).data

        if not request.user.is_superuser:
            targets = ['username', 'first_name', 'last_name', 'date_joined', 'email']
            userdata = {key: val for key, val in userdata.items() if key in targets}

        timestamp = datetime.timestamp(datetime.utcnow())
        return Response({'version': api_version, 'user': userdata, 'timestamp': timestamp})


from .action import *
from .readonly import *
from .readwrite import *
