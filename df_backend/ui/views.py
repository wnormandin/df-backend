from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from ..api import models, serializers
from . import forms


class FormIndexView(FormView):
    template_name = 'formindex.html'


class AutoCreatedByView(FormIndexView):

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)


class DefaultIndexView(TemplateView):
    template_name = 'index.html'


# Faction Views
class FactionDetailView(DetailView):
    model = models.EntityFaction
    template_name = 'faction/faction_detail.html'


class FactionListView(ListView):
    model = models.EntityFaction
    template_name = 'faction/faction_list.html'


class FactionFormView(AutoCreatedByView):
    form_class = forms.EntityFactionForm
    success_url = reverse_lazy('ui_factions')

    def form_valid(self, form):
        faction = form.create_faction(created_by=self.request.user)
        return redirect('ui_faction_detail', pk=faction.id)


# Profession Views
class ProfessionDetailView(DetailView):
    model = models.EntityProfession
    template_name = 'profession/profession_detail.html'


class ProfessionListView(ListView):
    model = models.EntityProfession
    template_name = 'profession/profession_list.html'


class ProfessionInputFormView(AutoCreatedByView):
    form_class = forms.ProfessionInputForm
    success_url = reverse_lazy('ui_professions')

    def form_valid(self, form):
        prof = form.create_profession(created_by=self.request.user)
        return redirect('ui_profession_detail', pk=prof.id)


# Race Views
class RaceDetailView(DetailView):
    model = models.EntityRace
    template_name = 'race/race_detail.html'


class RaceListView(ListView):
    model = models.EntityRace
    template_name = 'race/race_list.html'


class RaceInputFormView(AutoCreatedByView):
    form_class = forms.RaceInputForm

    def form_valid(self, form):
        race = form.create_race(created_by=self.request.user)
        return redirect('ui_race_detail', pk=race.id)


# Name/Language Views
class NamePartFormView(AutoCreatedByView):
    form_class = forms.NamePartForm
    success_url = reverse_lazy('ui_names')


class NameDomainFormView(AutoCreatedByView):
    form_class = forms.NameDomainForm
    success_url = reverse_lazy('ui_domains')


class NameLanguageFormView(AutoCreatedByView):
    form_class = forms.NameLanguageForm
    success_url = reverse_lazy('ui_namelangs')


class StatModifiersFormView(AutoCreatedByView):
    form_class = forms.StatModifiersForm
    success_url = reverse_lazy('ui_statmods')


# Log Views
class LogTypeFormView(AutoCreatedByView):
    form_class = forms.LogTypeForm
    success_url = reverse_lazy('ui_logtypes')


class ServerLogFormView(AutoCreatedByView):
    form_class = forms.ServerLogForm
    success_url = reverse_lazy('ui_logs')

