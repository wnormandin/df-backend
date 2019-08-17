from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

from ..serializers import UserSerializer
from df_backend import __version__ as api_version


class UserLogin(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'error': 'Must provide "username" and "password" values'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get_by_natural_key(request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'error': "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


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
