from django.urls import path
from core.views import index
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path("contact/", views.contact, name="contact"),
    path("account/", views.account, name="account"),       
    path("wishlist/", views.wishlist, name="wishlist"),     
    path("orders/", views.orders, name="orders"),
    path('products/', views.product_list_view, name='product_list'),
    path("product/<uuid:pid>/", views.product_detail_view, name="product_detail"),
    path('products/', views.all_products, name='all_products'), #view more
    path('category/', views.category_list_view, name='category_list'),
    path('category/<int:category_id>/', views.category_product_list_view, name='category_product_list'),
    path('vendors/', views.vendor_list_view, name='vendor_list'),
    path("vendor/<uuid:vid>/", views.vendor_detail_view, name="vendor_detail"),
    path("shop/", views.product_list_view, name="shop"),
    path("hot-deals/", views.hot_deals, name="hot_deals"),
    path("mega-menu/", views.mega_menu, name="mega_menu"),
    path("blog/", views.blog_list, name="blog"),
    path("pages/", views.pages, name="pages"),
    path("products/tag/<slug:tag_slug>/", views.tag_list_view, name="tag"),
    path("search/", views.search, name="search"),
    path('add-to-cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('pay/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
     path("pay/khalti/<int:order_id>/", views.khalti_payment),
    path("payment/success/", views.khalti_verify),
    path("payment/success/", views.khalti_success),
    path('verify-khalti/', views.verify_khalti, name='verify_khalti'),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),


]