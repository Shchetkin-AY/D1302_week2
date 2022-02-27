from random import sample

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from tours.data import tours, departures, title, subtitle, description


def main_view(request):
    hot_tours = dict(sample(tours.items(), 6))
    return render(request, 'tours/index.html', context={
        'departures': departures,
        'hot_tours': hot_tours,
        'title': title,
        'subtitle': subtitle,
        'description': description

    })


def departure_view(request, departure):
    filter_tours = {}
    from_departure = departures.get(departure)
    for key, item in tours.items():
        if item['departure'] == departure:
            filter_tours[key] = item
    min_price = min(item['price'] for price, item in filter_tours.items())
    max_price = max(item['price'] for price, item in filter_tours.items())
    min_nights = min(item['nights'] for price, item in filter_tours.items())
    max_nights = max(item['nights'] for price, item in filter_tours.items())
    count_tours = len(filter_tours)
    return render(request, 'tours/departure.html', context={
        'departures': departures,
        'from_departure': from_departure,
        'filter_tours': filter_tours,
        'count_tours': count_tours,
        'min_price': min_price,
        'max_price': max_price,
        'min_nights': min_nights,
        'max_nights': max_nights

    })


def tour_view(request, tour_id):
    tour = tours.get(tour_id)
    tour['departure'] = departures[tour['departure']]
    return render(request, 'tours/tour.html', context={'tour': tour, 'departures': departures})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
