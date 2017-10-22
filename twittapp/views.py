from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django import template
from django.template import *
import json
import requests


host='https://search-tweetmap-2wytbjehhdmbktm3g54w77zqly.us-east-2.es.amazonaws.com/cloud_tweet1/_search'


def index(request):
    if "key_word" in request.POST :
        value = request.POST["key_word"]
        print(value)
        if value :
            query = json.dumps({
			'size': 1000,
                "query": {
                    "match": {
                        "content": value
                    }
                }
            })
            result = requests.get(host, data=query)
            results = json.loads(result.text)
            tweetCoords = [dict() for num in range(len(results['hits']['hits']))]
            for idx, elements in enumerate(tweetCoords):
                originValue = results['hits']['hits'][idx]['_source']
                tempCoordinates = str(originValue['coordinates']).strip("'").strip('[').strip(']').split(',')
                tweetCoords[idx] = dict(lng=float(tempCoordinates[0]), lat=float(tempCoordinates[1]))
        return render(request, "tweet_map.html",{"lats":tweetCoords})

    else :
        value = None
    return render(request, "index.html", {'value': value})


def IndexPage(request):
    return render(request, "tweet_map.html")