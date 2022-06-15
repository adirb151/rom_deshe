from django.shortcuts import render
from .models import Query
from django.http import HttpResponse
from datetime import datetime
from .filters import QueryFilter


def query_list(request):
    queries = Query.objects.all().order_by('date')

    myFilter = QueryFilter(request.GET, queryset=queries)
    queries = myFilter.qs

    return render(request, r'queries/query_list.html', {'queries': queries, 'curr_date': datetime.now(), 'size': len(queries), 'myFilter': myFilter})

def query_detail(request, slug):
    query = Query.objects.get(slug=slug)
    return render(request, r'queries/query_detail.html', {'query': query})

def delete_query(request, slug):
    q = Query.objects.get(slug=slug)
    q.delete()
    queries = Query.objects.all().order_by('date')
    return render(request, r'queries/query_list.html', {'queries': queries, 'curr_date': datetime.now()})
