from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Shop, CartItem, Item, Cart
from .forms import ItemCountForm


class ShopListView(ListView):
    model = Shop
    template_name = 'main.html'
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.prefetch_related('items')

        return context


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Cart.objects.prefetch_related('cart_items').all().prefetch_related('item')

        return context


class ItemDetailView(DetailView):
    model = Item
    pk_url_kwarg = 'item_id'
    template_name = 'item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_form'] = ItemCountForm()
        context['message'] = ''

        return context

    def post(self, request, item_id, *args, **kwargs):
        customer = request.user.user_customer
        item = Item.objects.get(id=item_id)
        cart_item_list = CartItem.objects.select_related('customer').get(customer=customer).select_related('item').get(item=item)
        context = {'item': item, 'count_form': ItemCountForm(), 'message': ''}
        form = ItemCountForm(request.POST)
        if form.is_valid():
            price = item.price
            item_count = form.cleaned_data.get('item_count')
            cost = item_count * price
            if customer.account_balance >= cost:
                customer.account_balance -= cost
                customer.save()
                item.stock -= item_count
                item.save()
                cart.add_item(item, item_count)
            else:
                context['message'] = _('Your account does not have enough funds to payment')
                return render(request, 'item.html', context=context)

            context['message'] = _('Item has been added to the cart')
            return render(request, 'item.html', context=context)

        context['message'] = _('Item has not been added to the cart')
        return render(request, 'item.html', context=context)
