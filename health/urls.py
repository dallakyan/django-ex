from django.conf.urls import url

from health import views

medicine_id = '(?P<medicine_id>[^/]+)'
medicine_taken_id = '(?P<medicine_taken_id>[^/]+)'
sleep_id = '(?P<sleep_id>[^/]+)'
symptom_id = '(?P<symptom_id>[^/]+)'
symptom_occurrence_id = '(?P<symptom_occurrence_id>[^/]+)'

urlpatterns = [
    # Main views
    url(r'^$',
        views.main, name='health-main'),
    url(r'^view-as-chart/$',
        views.view_as_chart, name='health-view-chart'),
    url(r'^add-sleep/$',
        views.add_sleep, name='health-add-sleep'),
    url(r'^edit-sleep/'+sleep_id+'$',
        views.edit_sleep, name='health-edit-sleep'),
    url(r'^add-symptom/$',
        views.add_symptom, name='health-add-symptom'),
    url(r'^add-symptom-occurrence/$',
        views.add_symptom_occurrence, name='health-add-symptom-occurrence'),
    url(r'^add-symptom-occurrence/'+symptom_id+'$',
        views.add_symptom_occurrence, name='health-add-symptom-occurrence-w-id'),
    url(r'^edit-symptom-occurrence/'+symptom_occurrence_id+'$',
        views.edit_symptom_occurrence, name='health-edit-symptom-occurrence'),
    url(r'^add-medicine/$',
        views.add_medicine, name='health-add-medicine'),
    url(r'^add-medicine-taken/$',
        views.add_medicine_taken, name='health-add-medicine-taken'),
    url(r'^add-medicine-taken/'+medicine_id+'$',
        views.add_medicine_taken, name='health-add-medicine-taken-w-id'),
    url(r'^edit-medicine-taken/'+medicine_taken_id+'$',
        views.edit_medicine_taken, name='health-edit-medicine-taken'),
]

# vim: et sw=4 sts=4
