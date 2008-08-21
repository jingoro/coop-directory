from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from coops.models import Coop
from django import forms

class CoopForm(forms.Form):
    name = forms.CharField(max_length = 50)
    address = forms.CharField()
    phone = forms.CharField(required = False)
    email = forms.EmailField(required = False)

    # Google App models expect None instead of '' for empty fields, unlike Django models.
    def cleaner_data(self):
        results = self.cleaned_data.copy()
        for key in results:
            if results[key] == '' or results[key] == u'':
                results[key] = None
        return results
    
def coop_detail(request, id):
    coop = get_object_or_404(Coop, pk = id)
    return render_to_response('coops/detail.html', {'coop': coop})

def coop_add(request):
    if request.method == 'POST':
        post = request.POST
    else:
        post = None
    form = CoopForm(post, auto_id = True)
    if form.is_valid():
        c = Coop(**form.cleaner_data())
        c.put()
        return HttpResponseRedirect('/')
    return render_to_response('coops/add.html', {'form': form})

def coop_list(request):
    # TODO: parse GET search parameters
    coops = Coop.all().order('-modified')
    paginator = Paginator(coops, 10)
    page = paginator.page(request.GET.get('p', 1))
    return render_to_response('coops/list.html', {
        'page': page,
        'querystring': '',
        'first_item_number': paginator.per_page * (page.number - 1) + 1
    })

def index(request):
    return HttpResponse("Testing 123")
