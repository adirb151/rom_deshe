from django.shortcuts import render
from .models import Query
from django.http import HttpResponse


def query_list(request):
    queries = Query.objects.all().order_by('date')
    return render(request, r'queries/query_list.html', {'queries': queries})

def query_detail(request, slug):
    query = Query.objects.get(slug=slug)
    return render(request, r'queries/query_detail.html', {'query': query})
