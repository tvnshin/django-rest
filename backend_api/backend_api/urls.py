"""
URL configuration for backend_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from accounts.views import RegisterView
from products.views import *
from cart.views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),

    #auth
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),

    #api
    path('api/cart/', CartItemsView.as_view()),
    path('api/cart/info/', CartView.as_view()),
    path('api/products/', ProductsView.as_view(), name='product-list'),
    path('api/products/<int:product_id>/', SingleProductView.as_view()),
    path('api/cart/item/<int:item_id>/', CartItemsView.as_view(), name='cart-item-update'),
    path('api/cart/item/delete/<int:cart_item_id>/', CartItemDeleteView.as_view()),
    path('api/products/category/<str:category_name>/', CategoryView.as_view(), name='category_view'),
]
