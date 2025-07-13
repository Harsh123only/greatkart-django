from django.urls import path
from .import views

urlpatterns = [
    path("",views.storee,name='store'),
    path("category/<slug:category_slug>/",views.storee,name='product_by_category'),
    path("category/<slug:category_slug>/<slug:product_slug>/",views.product_detail,name='product_detail'),
    path("search/", views.search, name='search'),
    # path("search/<slug:category_slug>/", views.search, name='search_by_category'),
    # path("search/<slug:category_slug>/<slug:product_slug>/", views.product_detail, name='product_detail_by_search'),

    
]
