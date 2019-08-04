
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


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


from .action import *
from .readonly import *
from .readwrite import *
