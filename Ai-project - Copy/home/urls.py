from django.urls import path

from .views import create_product, get_item, homepage,aboutus,contactus,update_product,delete_product

urlpatterns=[
    path('',homepage,name="products"),
    path('about/',aboutus,name="about"),
    path('contact/',contactus,name="contact"),
    path('product/<int:id>/',get_item,name="product"),
    path('create/',create_product,name="create_product"),
    path('update/<int:id>/',update_product,name="update_product"),
    path('delete/<int:id>/',delete_product,name="delete_product"),
    
]



