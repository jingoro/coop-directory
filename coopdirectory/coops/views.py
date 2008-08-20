from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404
from coopdirectory.coops.models import Coop

def coop_detail(request, id):
    coop = get_object_or_404(Coop, pk = id)
    return render_to_response('coops/detail.html', {'coop': coop})

def coop_list(request):
    # TODO: parse GET search parameters
    coops = Coop.objects.all()
    paginator = Paginator(coops, 10)
    page = paginator.page(request.GET.get('p', 1))
    return render_to_response('coops/list.html', {'page': page, 'querystring': '', 'first_item_number': paginator.per_page * (page.number - 1) + 1})



