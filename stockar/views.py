from django.shortcuts import render

from stockar.models import StorageOffer


def index(request):
    context = {
        'offers': list(StorageOffer.objects.all())
    }

    return render(request, 'index.html', context)
