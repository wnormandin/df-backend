from django.urls import path

from . import views


urlpatterns = [
    path(r'', views.DefaultIndexView.as_view(), name='ui_index'),
    path(r'factions/new', views.FactionFormView.as_view(), name='ui_factions_new'),
    path(r'nameparts/new', views.NamePartFormView.as_view(), name='ui_names_new'),
    path(r'namedoms/new', views.NameDomainFormView.as_view(), name='ui_domains_new'),
    path(r'namelangs/new', views.NameLanguageFormView.as_view(), name='ui_namelangs_new'),
    path(r'statmods/new', views.StatModifiersFormView.as_view(), name='ui_statmods_new'),
    path(r'logtypes/new', views.LogTypeFormView.as_view(), name='ui_logtypes_new'),
    path(r'logs/new', views.ServerLogFormView.as_view(), name='ui_logs_new'),
    path(r'professions/new', views.ProfessionInputFormView.as_view(), name='ui_professions_new'),
    path(r'races/new', views.RaceInputFormView.as_view(), name='ui_races_new'),
    path(r'races', views.RaceListView.as_view(), name='ui_races'),
    path(r'races/<int:pk>', views.RaceDetailView.as_view(), name='ui_race_detail'),
    path(r'professions', views.ProfessionListView.as_view(), name='ui_professions'),
    path(r'professions/<int:pk>', views.ProfessionDetailView.as_view(), name='ui_profession_detail'),
    path(r'factions', views.FactionListView.as_view(), name='ui_factions'),
    path(r'factions/<int:pk>', views.FactionDetailView.as_view(), name='ui_faction_detail'),
]

