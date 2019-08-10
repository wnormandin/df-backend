from django.urls import include, path, re_path
from rest_framework import routers
from . import views


# Viewset router
router = routers.SimpleRouter(trailing_slash=False)
router.register('races', views.RaceViewSet)
router.register('professions', views.ProfessionViewSet)
router.register('factions', views.FactionViewSet)
router.register('entities', views.EntityViewSet)
router.register('names', views.NamePartViewSet)

# Name-related APIViews
name_patterns = [
    path(r'domains', views.NameDomainList.as_view()),
    path(r'languages', views.LanguagesList.as_view()),
    path(r'eras', views.NameEraList.as_view()),
    path(r'generate', views.RandomNameGeneration.as_view())
]

# Character generation APIViews
generate_patterns = [
    re_path(r'names/?(?P<count>\d+)?/?', views.RandomNameGeneration.as_view()),
    path(r'entities', views.GetEntities.as_view())
]

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'register', views.RegisterUser.as_view()),
    path(r'races', views.RaceList.as_view()),
    path(r'professions', views.ProfessionList.as_view()),
    path(r'factions', views.FactionList.as_view()),
    path(r'entities', views.EntityList.as_view()),
    path(r'api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path(r'name/', include(name_patterns)),
    path(r'generate/', include(generate_patterns))
]
