from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django import forms

from collections import namedtuple
from datetime import datetime, timedelta

from health.models import *
from health.settings import template_base

@login_required
def main(request):
    data = base_data()
    return render(request, template_base + 'main.html', data)


def base_data():
    data = {}
    data['symptoms'] = Symptom.objects.all()
    data['medicines'] = Medicine.objects.all()
    data['sleep'] = Sleep.objects.all()
    data['urls'] = []
    return data


def add_url_to_data(data, varname, link):
    Url = namedtuple('Url', ['varname', 'link'])
    data['urls'].append(Url(varname, link))


@login_required
def view_as_chart(request):
    data = base_data()
    data['now'] = datetime.now()
    return render(request, template_base + 'chart.html', data)


@login_required
def add_symptom(request):
    return simple_form(request, SymptomForm, reverse('health-main'),
            'Add Symptom', 'Add Symptom')


@login_required
def add_symptom_occurrence(request, symptom_id=None):
    i = {}
    if symptom_id:
        symptom = get_object_or_404(Symptom, pk=symptom_id)
        i['symptom'] = symptom
    return simple_form(request, SymptomOccurrenceForm, reverse('health-main'),
            'Add Symptom Occurrence', 'Add Symptom Occurrence', initial=i)


@login_required
def edit_symptom_occurrence(request, symptom_occurrence_id):
    s = get_object_or_404(SymptomOccurrence, pk=symptom_occurrence_id)
    return simple_form(request, SymptomOccurrenceForm, reverse('health-main'),
            'Edit Symptom Occurrence', 'Edit Symptom Occurrence', instance=s)


@login_required
def add_sleep(request):
    return simple_form(request, SleepForm, reverse('health-main'),
            'Add Sleep', 'Add Sleep')


@login_required
def edit_sleep(request, sleep_id):
    s = get_object_or_404(Sleep, pk=sleep_id)
    return simple_form(request, SleepForm, reverse('health-main'),
            'Add Sleep', 'Add Sleep', instance=s)


@login_required
def add_medicine(request):
    return simple_form(request, MedicineForm, reverse('health-main'),
            'Add Medicine', 'Add Medicine')


@login_required
def add_medicine_taken(request, medicine_id=None):
    i = {}
    if medicine_id:
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        i['medicine'] = medicine
    data = base_data()
    data['extra_form_elements'] = [add_dose_button(), add_dose_form()]
    add_url_to_data(data, 'create_dose', reverse('food-create-quantity-ajax'))
    return simple_form(request, MedicineTakenForm, reverse('health-main'),
            'Add Medicine Taken', 'Add Medicine Taken', initial=i, data=data)


@login_required
def edit_medicine_taken(request, medicine_taken_id):
    m = get_object_or_404(MedicineTaken, pk=medicine_taken_id)
    data = base_data()
    data['extra_form_elements'] = [add_dose_button(), add_dose_form()]
    add_url_to_data(data, 'create_dose', reverse('food-create-quantity-ajax'))
    return simple_form(request, MedicineTakenForm, reverse('health-main'),
            'Edit Medicine Taken', 'Edit Medicine Taken', instance=m, data=data)


@login_required
def simple_form(request, form_class, next_url, label, header, instance=None,
        initial={}, data=None):
    if request.POST:
        if instance:
            form = form_class(request.POST, instance=instance)
        else:
            form = form_class(request.POST)
        form.save()
        return HttpResponseRedirect(next_url)
    if data == None:
        data = base_data()
    data['form'] = form_class(instance=instance, initial=initial)
    data['submit_label'] = label
    data['header'] = header
    return render(request, 'add_form.html', data)


class DateTimeWidget(forms.DateTimeInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datetimepicker'}
        if 'format' not in self.attrs:
            self.attrs['format'] = '%m/%d/%Y %I:%M %p'

    def render(self, name, value, attrs=None):
        if value:
            value = value.strftime(self.attrs['format'])
        return super(forms.DateTimeInput, self).render(name, value, attrs)

FORMATS = ['%m/%d/%Y %I:%M %p']


class SleepForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=FORMATS,
                                     widget=DateTimeWidget())
    end_time = forms.DateTimeField(input_formats=FORMATS,
                                   widget=DateTimeWidget())
    class Meta:
        model = Sleep
        fields = '__all__'


class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = '__all__'


class SymptomOccurrenceForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=FORMATS,
                                     widget=DateTimeWidget())
    end_time = forms.DateTimeField(input_formats=FORMATS,
                                   widget=DateTimeWidget())
    class Meta:
        model = SymptomOccurrence
        fields = '__all__'


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'


class MedicineTakenForm(forms.ModelForm):
    time = forms.DateTimeField(input_formats=FORMATS, widget=DateTimeWidget())
    class Meta:
        model = MedicineTaken
        fields = '__all__'


def add_dose_button():
    button = '<button id="add_dose_button">'
    button += 'Add Dose'
    button += '</button>'
    return button


def add_dose_form():
    input_classes = 'text ui-widget-content ui-corner-all'
    form = '<div id="add_dose_form">'
    form += '<form>'
    form += '<fieldset>'
    form += '<label for="amount">Amount</label>'
    form += '<input type="text" name="amount" id="id_amount" class="'
    form += input_classes + '">'
    form += '<label for="measure">Measure</label>'
    form += '<input type="text" name="measure" id="id_measure" class="'
    form += input_classes + '">'
    form += '</fieldset>'
    form += '</form>'
    form += '</div>'
    return form
