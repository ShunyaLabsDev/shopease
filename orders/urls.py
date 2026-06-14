from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path("my-orders/", views.order_list, name="order_list"),
    path("my-orders/<str:order_number>/", views.order_detail, name="order_detail"),
    path("success/<str:order_number>/", views.order_success, name="order_success"),
]
