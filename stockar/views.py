from django.shortcuts import render

from stockar.models import StorageOffer


def index(request):
    context = {}

    return render(request, 'index.html', context)


def offers(request):
    context = {
        'offers': list(StorageOffer.objects.filter(active=True).order_by('-added_at')),
    }

    return render(request, 'offers.html', context)
