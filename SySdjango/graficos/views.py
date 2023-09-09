from django.shortcuts import render
from django.http.response import JsonResponse
from random import randrange

# Create your views here.

def get_chart(_request):
    data = {
        "xAxis": {
            "type": "category",
            "data": ["A", "B", "C", "D", "E"]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "data": [10, 20, 15, 30, 25],
                "type": "bar"
            }
        ]
    }
    return JsonResponse(data)
