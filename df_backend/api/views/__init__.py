from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from ..serializers import UserSerializer
from df_backend import __version__ as api_version


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
            targets = ['username', 'first_name', 'last_name', 'date_joined']
            userdata = {key: val for key, val in userdata.items() if key in targets}

        timestamp = datetime.timestamp(datetime.utcnow())
        return Response({'version': api_version, 'user': userdata, 'timestamp': timestamp})


from .action import *
from .readonly import *
from .readwrite import *
