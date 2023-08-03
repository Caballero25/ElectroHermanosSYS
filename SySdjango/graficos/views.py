from django.shortcuts import render
from django.http.response import JsonResponse
from random import randrange

# Create your views here.

def get_chart(_request):

    color = 'green'

    serie = [122, 170, 250, 300, 150, 170, 200]

    chart = {
        'tooltip': {
            'show': True,
            'trigger': 'axis',
            'triggerOn': 'mousemove|click'
        },
        'xAxis': [
            {
                "type": "category",
                "data": ["Mon","Tue","Wed","Thu", "Fri", "Sat", "Sun"]
            }
        ],
        'yAxis': [
            {
                "type": "value"
            }
        ],
        'series':[
            {
                'data':serie,
                'type': "line",
                'itemStyle': {
                    'color': color,  
                },
                'lineStyle': {
                    'color': color,
                }
            }
        ]
    }
    return JsonResponse(chart)
