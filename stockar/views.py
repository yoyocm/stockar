import stripe
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from stockar.forms import AccountCreationForm
from stockar.models import StorageOffer, Account


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


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = stripe.Price.list(product=self.kwargs["pk"])['data'][0]
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            customer=stripe.Customer.retrieve(Account.objects.get(email=request.user).stripe_customer_id),
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/'
        )
        return redirect(checkout_session.url)
