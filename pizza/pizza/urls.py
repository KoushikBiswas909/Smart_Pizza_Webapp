"""pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import *

urlpatterns = [
    path('', home),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('add-cart/<pizza_uid>/', add_cart, name="add_cart"),
    path('cart/', cart, name="cart"),
    path('remove_cart_items/<cart_item_uid>',
         remove_cart_items, name="remove_cart_items"),
    path('orders/', orders, name="orders"),
    path('success/', success, name="success"),
    path('admin/', admin.site.urls),
    path('predict/', predict, name="predict"),
    path('predict/result', result, name="result"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
