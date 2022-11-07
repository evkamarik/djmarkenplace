from django.urls import path
from django.views.decorators.cache import cache_page
from .views import ShopListView, CartDetailView, ItemDetailView


urlpatterns = [
    path('', ShopListView.as_view(), name='main'),
    path('cart/<int:pk>', CartDetailView.as_view(), name='cart'),
    path('item/<int:item_id>', cache_page(5000)(ItemDetailView.as_view()), name='item'),
]
