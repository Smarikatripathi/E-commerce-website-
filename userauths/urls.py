# maps a URL path to the view.Without this, Django doesn’t know which view to show for the signup page.

from django.urls import path
from . import views

app_name = "userauths"  # IMPORTANT for namespacing

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('orders/', views.orders_view, name='orders'),
    path('vouchers/', views.vouchers_view, name='vouchers'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('settings/', views.settings_view, name='settings'),
]
