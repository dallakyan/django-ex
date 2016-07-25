from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from django import forms

from visits.models import Visit, Provider, File



# Forms
class VisitForm(forms.ModelForm):
    providers = forms.ModelMultipleChoiceField(queryset=Provider.objects.all())

    class Meta:
        model = Visit


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        exclude = ['user', 'visits']


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['user', 'visit']



# Views
def logout_view(request):
    logout(request)
    return HttpResponse("logged out")

def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})


from django.core.mail import send_mail

def mail_view(self):
    send_mail('Subject here', 'Here is the message.', 'from@example.com',
              ['maxchgr@gmail.com'], fail_silently=False)
    return HttpResponse("thanks for the email")


class ProviderList(ListView):

    template_name = 'visits/provider_list.html'

    def get_queryset(self):
        return self.request.user.provider_set.all()


class VisitList(ListView):

    template_name = 'visits/visit_list.html'
    model = Visit

    def get_queryset(self):
        return self.request.user.visit_set.all()

    def get_context_data(self, **kwargs):
        context = super(VisitList, self).get_context_data(**kwargs)
        context['providers'] = self.request.user.provider_set.all()
        return context


class VisitDetail(DetailView):

    model = Visit
    template_name = 'visits/visit_detail.html'

    def get_object(self):
        visit = super(VisitDetail, self).get_object()
        if visit.user == self.request.user:
            return visit
        else:
            raise PermissionDenied


class VisitCreate(View):

    def get_visit_object(self):
        visit_id = self.kwargs.get('pk', False)
        if visit_id:
            visit = Visit.objects.get(id=visit_id)
        else:
            visit = None
        return visit

    def get(self, request, **kwargs):
        visit = self.get_visit_object()

        p_form = ProviderForm(prefix="pform")
        v_form = VisitForm(prefix="vform", instance=visit)
        v_form.fields['providers'].initial = visit.provider_set.all() if visit else visit
        i_form = UploadFileForm()

        context = {'p_form': p_form, 'v_form': v_form, 'i_form': i_form}
        return render(request, 'visits/visit_create.html', context)

    def post(self, request, **kwargs):
        visit = self.get_visit_object()

        p_form = ProviderForm(request.POST, prefix="pform")
        v_form = VisitForm(request.POST, prefix="vform", instance=visit)
        i_form = UploadFileForm(request.POST, request.FILES) if request.FILES else None

        if 'pform-submit' in request.POST.keys():
            if p_form.is_valid():
                p = p_form.save(commit=False)
                p.user = self.request.user
                p.save()
                return redirect('index')
        elif 'vform-submit' in request.POST.keys():
            if v_form.is_valid():
                v = v_form.save()
                p = v_form.cleaned_data['providers']
                v.provider_set.add(*p)
                v.save()
                if i_form and i_form.is_valid():
                    i = i_form.save(commit=False)
                    i.visit = v
                    i.user = self.request.user
                    i.save()
                return redirect('index')

        context = {'p_form': p_form, 'v_form': v_form, 'i_form': i_form}
        return render(request, 'visits/visit_create.html', context)
