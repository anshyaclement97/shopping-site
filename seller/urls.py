from django.urls import path
from .views import *

urlpatterns = [
    path('sellerreg/',register_sellers),
    path('orderlist/',order_list),

    path('register/', register_seller),
    path('login/', login_view)
    ]

