from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

@login_required
def main(request):
    context = RequestContext(request)
    return render_to_response('main.html', context)

# vim: et sw=4 sts=4
