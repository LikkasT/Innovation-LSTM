"""
URL configuration for Innovation_LSTM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from testapp import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/create_user/', views.create_user),
    path('api/runback/', views.runback),
    path('api/user_login/', views.user_login),
    path('api/user_modify/', views.user_modify),
    path('api/user_avatar', views.user_avatar),
    path('api/collection/', views.collection),
    path('api/goods_show/', views.goods_show),
    path('api/trading_hot_list/', views.trading_hot_list),
    path('api/earnings_ranking/', views.earnings_ranking),
    path('api/search/', views.search),

    path('api/history/', views.history),
]
