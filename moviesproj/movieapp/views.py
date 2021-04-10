from django.shortcuts import render
import imdb
import requests
from django.http import HttpResponse, Http404
import json
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
def data_search(request):
    context = {}
    if request.method == 'POST':

        url = settings.X_RAPIDAPI_BASE_URL
        name = request.POST['search']
        print(request.POST['search'])
        url = url + f"?s={ request.POST['search'] }&page=1&r=json"
        print(url)

        headers = {
            'x-rapidapi-key': settings.X_RAPIDAPI_KEY,
            'x-rapidapi-host': settings.X_RAPIDAPI_HOST,
            'useQueryString': 'true',
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "upload_date": "",
            "read": "True"
        })

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            context = {
                'movie_list': response.json()['Search']
            }

        except Exception as e:
            return render(request, 'Error.html')

    return render(request, 'search.html', context)


def Trailer(request):
        
    imdb = request.GET.get('imdb', -1)
    title = request.GET.get('title', -1)
    context = {}
    print(type(title),'**', title,type(imdb),imdb)

    trailerUrl = ""
    try:             
        params = {
            'part': "snippet",
            'q': title + " official trailer",
            'key': settings.YOUTUBE_API_KEY
        }
        result = requests.get(settings.YOUTUBE_API_BASE_URL, params=params)
        data = result.json()['items'][0]['id']['videoId']
        print(data)
        trailerUrl = settings.YOUTUBE_BASE_URL + result.json()['items'][0]['id']['videoId']

    except Exception as e:
        print("Trailer does not exist")

    try:
        url = settings.X_RAPID_API_BASE_URL_ID
        querystring = {"type": "get-movie-details", "imdb": imdb}
        headers = {
            'x-rapidapi-key': settings.X_RAPIDAPI_KEY,
            'x-rapidapi-host': settings.X_RAPID_API_HOST_NAME_ID,
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.json())

    except Exception as e:
        print("Info not found")
        return render(request, 'Error.html') 

    context = {
        'trailerUrl' : trailerUrl,
        'movieDetails' : response.json(),
        'movieTitle' : title
    }

    return render(request, 'Trailer.html', context)
