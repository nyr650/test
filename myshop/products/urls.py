from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('product/', views.product_detail, name='product_detail'),

    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('search/', views.search, name='search'),
    path('categories/', views.category_list, name='category_list'),
]






