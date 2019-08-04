from django import forms
from django_select2.forms import Select2MultipleWidget

from ..api import models
from ..utils import constants


class EntityFactionForm(forms.ModelForm):
    class Meta:
        model = models.EntityFaction
        exclude = ('created_by',)


class NamePartForm(forms.ModelForm):
    class Meta:
        model = models.NamePart
        exclude = ('created_by',)


class NameLanguageForm(forms.ModelForm):
    class Meta:
        model = models.NameLanguage
        exclude = ('created_by',)


class NameEraForm(forms.ModelForm):
    class Meta:
        model = models.NameEra
        exclude = ('created_by',)


class NameDomainForm(forms.ModelForm):
    class Meta:
        model = models.NameDomain
        exclude = ('created_by',)


class StatModifiersForm(forms.ModelForm):
    class Meta:
        model = models.StatModifiers
        exclude = ('created_by',)


class LogTypeForm(forms.ModelForm):
    class Meta:
        model = models.LogType
        exclude = ('created_by',)


class ServerLogForm(forms.ModelForm):
    class Meta:
        model = models.ServerLog
        exclude = ('created_by',)


class RaceForm(forms.Form):
    name = forms.CharField(label='Race Name', max_length=100)
    description = forms.CharField(label='Race Description', max_length=1000, widget=forms.Textarea)


class ProfessionForm(forms.Form):
    name = forms.CharField(label='Profession Name', max_length=100)
    description = forms.CharField(label='Profession Description', max_length=1000, widget=forms.Textarea)
    races = forms.ModelMultipleChoiceField(queryset=models.EntityRace.objects.all(),
                                           widget=Select2MultipleWidget)


# Non-model form for linked input (e.g. during entity creation)
class StatForm(forms.Form):
    food = forms.IntegerField(label='Food', min_value=0, max_value=255)
    drink = forms.IntegerField(label='Drink', min_value=0, max_value=255)
    stamina = forms.IntegerField(label='Stamina', min_value=0, max_value=255)
    toughness = forms.IntegerField(label='Toughness', min_value=0, max_value=255)
    agility = forms.IntegerField(label='Agility', min_value=0, max_value=255)
    dexterity = forms.IntegerField(label='Dexterity', min_value=0, max_value=255)
    intelligence = forms.IntegerField(label='Intelligence', min_value=0, max_value=255)
    wisdom = forms.IntegerField(label='Wisdom', min_value=0, max_value=255)
    charm = forms.IntegerField(label='Charm', min_value=0, max_value=255)
    persuasion = forms.IntegerField(label='Persuasion', min_value=0, max_value=255)
    introversion = forms.IntegerField(label='Introversion', min_value=0, max_value=255)
    stability = forms.IntegerField(label='Stability', min_value=0, max_value=255)
    friendliness = forms.IntegerField(label='Friendliness', min_value=0, max_value=255)
    elements = forms.IntegerField(label='Elements', min_value=0, max_value=255)
    physical = forms.IntegerField(label='Physical', min_value=0, max_value=255)
    magic = forms.IntegerField(label='Magic', min_value=0, max_value=255)
    hunger = forms.IntegerField(label='Hunger', min_value=0, max_value=255)
    thirst = forms.IntegerField(label='Thirst', min_value=0, max_value=255)
    exhaustion = forms.IntegerField(label='Exhaustion', min_value=0, max_value=255)
    stress = forms.IntegerField(label='Stress', min_value=0, max_value=255)
    happiness = forms.IntegerField(label='Happiness', min_value=0, max_value=255)
    addiction = forms.IntegerField(label='Addiction', min_value=0, max_value=255)

    @property
    def stat_fields(self):
        return {field: getattr(self.cleaned_data, field) for field in constants.CORE_STATS}


class StatModForm(forms.Form):
    food = forms.IntegerField(label='Food modifier', min_value=-100, max_value=100)
    drink = forms.IntegerField(label='Drink modifier', min_value=-100, max_value=100)
    stamina = forms.IntegerField(label='Stamina modifier', min_value=-100, max_value=100)
    toughness = forms.IntegerField(label='Toughness modifier', min_value=-100, max_value=100)
    agility = forms.IntegerField(label='Agility modifier', min_value=-100, max_value=100)
    dexterity = forms.IntegerField(label='Dexterity modifier', min_value=-100, max_value=100)
    intelligence = forms.IntegerField(label='Intelligence modifier', min_value=-100, max_value=100)
    wisdom = forms.IntegerField(label='Wisdom modifier', min_value=-100, max_value=100)
    charm = forms.IntegerField(label='Charm modifier', min_value=-100, max_value=100)
    persuasion = forms.IntegerField(label='Persuasion modifier', min_value=-100, max_value=100)
    introversion = forms.IntegerField(label='Introversion modifier', min_value=-100, max_value=100)
    stability = forms.IntegerField(label='Stability modifier', min_value=-100, max_value=100)
    friendliness = forms.IntegerField(label='Friendliness modifier', min_value=-100, max_value=100)
    elements = forms.IntegerField(label='Elements modifier', min_value=-100, max_value=100)
    physical = forms.IntegerField(label='Physical modifier', min_value=-100, max_value=100)
    magic = forms.IntegerField(label='Magic modifier', min_value=-100, max_value=100)
    hunger = forms.IntegerField(label='Hunger modifier', min_value=-100, max_value=100)
    thirst = forms.IntegerField(label='Thirst modifier', min_value=-100, max_value=100)
    exhaustion = forms.IntegerField(label='Exhaustion modifier', min_value=-100, max_value=100)
    stress = forms.IntegerField(label='Stress modifier', min_value=-100, max_value=100)
    happiness = forms.IntegerField(label='Happiness modifier', min_value=-100, max_value=100)
    addiction = forms.IntegerField(label='Addiction modifier', min_value=-100, max_value=100)

    @property
    def stat_fields(self):
        return {field: self.cleaned_data[field] for field in constants.CORE_STATS}


class RaceInputForm(RaceForm, StatModForm):
    """ Form encapsulating inputs for a new race """

    def create_race(self, created_by):
        stat_args = {
            'name': self.cleaned_data['name'],
            'description': f'Stat modifiers for Race {self.cleaned_data["name"]}',
            **self.stat_fields
        }
        stat_mods = models.StatModifiers.objects.create(created_by=created_by, **stat_args)
        return models.EntityRace.objects.create(name=self.cleaned_data['name'],
                                                description=self.cleaned_data['description'],
                                                stats=stat_mods,
                                                created_by=created_by)

    def edit_race(self):
        pass


class ProfessionInputForm(ProfessionForm, StatModForm):
    """ Form encapsulating inputs for a new profession """

    def create_profession(self, created_by):
        stat_args = {
            'name': self.cleaned_data['name'],
            'description': f'Stat modifiers for Profession {self.cleaned_data["name"]}',
            **self.stat_fields
        }
        stat_mods = models.StatModifiers.objects.create(created_by=created_by, **stat_args)
        return models.EntityProfession.objects.create(name=self.cleaned_data['name'],
                                                      description=self.cleaned_data['description'],
                                                      stats=stat_mods,
                                                      created_by=created_by)

    def edit_race(self):
        pass
