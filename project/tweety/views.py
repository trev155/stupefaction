from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .twitter import search, util

def index(request):
    return render(request, 'tweety/index.html')


def tweet_search(request, query, num_results):
    data = search.twitter_search(query, num_results)
    data = util.simple_data_entries(data)

    return JsonResponse(data, safe=False)
