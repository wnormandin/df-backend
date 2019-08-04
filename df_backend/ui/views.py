from django.shortcuts import render
from django.http import HttpResponseRedirect


from ..api import models, serializers
from . import forms

# Create your views here.
def create_race(request):
    if request.method == 'POST':
        race_form = forms.RaceForm
        stat_form = forms.StatForm