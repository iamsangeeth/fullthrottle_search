from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import operator

def home(request):
    return render(request, 'home.html', {})

def search(request):
    if request.is_ajax():
        query = request.GET.get('word','')
        print(query)
        result_list = search_word(query)
        data = json.dumps(result_list)
    else:
        data = 'fail'
    type = 'application/json'
    return HttpResponse(data, type)

def results(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            result = search_word(query)
            if len(result) == 0:
                return JsonResponse({'search_result': "not found."})
            else:
                return JsonResponse({'search_result': result})
        else:
            return redirect('/')
    return 

def search_word(query):
    word_count = {}
    words = []
    results = []
    with open('word_search.tsv') as datafile:
        for row in datafile:
            word, frequency = row.split('\t')
            word_count[word] = int(frequency.strip())
            words.append(word)
    for word in words:
        if query.lower() in word:
            results.append(word)
    word_dict = [(result, result.find(query.lower()), word_count[result], len(result)) for result in results]
    word_dict.sort(key=operator.itemgetter(1))
    word_dict.sort(key=operator.itemgetter(3))
    search_result = [word_list[0] for word_list in word_dict][:25]
    return search_result