from django.urls import path
from django.views.decorators.cache import cache_page
from .views import register_view, ShopLoginView, ShopLogoutView, UserDetailView


urlpatterns = [
    path('register/', cache_page(5000)(register_view), name='register'),
    path('logout/', ShopLogoutView.as_view(), name='logout'),
    path('login/', cache_page(5000)(ShopLoginView.as_view()), name='login'),
    path('account/<int:customer_id>', cache_page(5000)(UserDetailView.as_view()), name='account'),
]
