from django.urls import path
from .views import *
urlpatterns=[
path('registration/',registration),
path('index/',index),
    path('userlogin/',userlogin),
    path('userprofile/',userprofile),
    path('updateprofile/<int:id>',updateprofile),
    path('sellerproductupload/',sellerproductupload),
    path('addtocart/<int:itemid>',addtocart),
    path('cartdisplay/',cartdisplay),
    path('incdec/<int:cartid>',inc_dec),
    path('addaddress/',addaddress),
    path('delivery_details/',delivery_details),
    path('final_summary/',final_summary),
    path('create_order/',create_order),
    path('logout/',logout),


    path('order_view/',order_view),



]