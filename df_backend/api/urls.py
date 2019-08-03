from django.urls import include, path, re_path
from rest_framework import routers
from . import views


router = routers.SimpleRouter(trailing_slash=False)
router.register('races', views.RaceViewSet)
router.register('professions', views.ProfessionViewSet)
router.register('factions', views.FactionViewSet)
router.register('entities', views.EntityViewSet)
router.register('names', views.NamePartViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    re_path(r'generate/names/?(?P<count>\d+)?/?', views.RandomNameGeneration.as_view()),
    path(r'races', views.RaceList.as_view()),
    path(r'professions', views.ProfessionList.as_view()),
    path(r'factions', views.FactionList.as_view()),
    path(r'entities', views.EntityList.as_view()),
    path(r'api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
