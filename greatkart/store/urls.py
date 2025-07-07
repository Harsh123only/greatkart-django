from django.urls import path
from .import views

urlpatterns = [
    path("",views.storee,name='store'),
    path("<slug:category_slug>/",views.storee,name='product_by_category'),
    path("<slug:category_slug>/<slug:product_slug>/",views.product_detail,name='product_detail')
    
]
