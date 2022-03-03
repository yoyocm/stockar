from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from stockar.forms import AccountCreationForm
from stockar.models import StorageOffer


def index(request):
    context = {}

    return render(request, 'index.html', context)


def offers(request):
    context = {
        'offers': list(StorageOffer.objects.filter(active=True).order_by('-added_at')),
    }

    return render(request, 'offers.html', context)


def signup(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save()
            login(request, account)
            return redirect('index')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid informations.')

    form = AccountCreationForm()
    return render(request, 'signup.html', {'form': form})
