from django.shortcuts import render
from django.http.response import JsonResponse
from random import randrange

# Create your views here.

def grafico(request):
    return render(request, 'graficos.html')

def get_chart(_request):

    colors = ['blue', 'orange', 'red', 'yellow', 'green']
    random_color = colors[randrange(0, (len(colors)-1))]

    serie = []
    counter = 0

    while(counter<7):
        serie.append(randrange(100,400))
        counter += 1

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
                    'color': random_color,  
                },
                'lineStyle': {
                    'color': random_color
                }
            }
        ]
    }
    return JsonResponse(chart)
