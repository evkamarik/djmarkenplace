import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Customer
from app_shop.models import Cart
from .forms import RegisterForm, CustomerBalanceForm
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _


@cache_page(300)
def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')
            customer = Customer.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address
            )
            Cart.objects.create(customer=customer)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('shop:main')

    return render(request, 'register.html', {'form': RegisterForm()})


class ShopLoginView(LoginView):
    template_name = 'login.html'


class ShopLogoutView(LogoutView):
    next_page = 'shop:main'


class UserDetailView(DetailView):
    model = Customer
    pk_url_kwarg = 'customer_id'
    template_name = 'account.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance_form'] = CustomerBalanceForm()
        context['message'] = ''

        return context


    def post(self, request, customer_id, *args, **kwargs):
        customer = Customer.objects.get(id=customer_id)
        context = {'customer': customer, 'balance_form': CustomerBalanceForm(), 'message': ''}
        form = CustomerBalanceForm(request.POST)
        if form.is_valid():
            customer.balance += form.cleaned_data.get('balance')
            customer.save()
            context['message'] = _('Your account is replenished')
        else:
            context['message'] = _('Your account is not replenished. Try again.')

        return render(request, 'account.html', context=context)




