"""stvapp URL Configuration

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
from django.urls import path
from .views import *


urlpatterns = [
    path('', campaign_list, name='campaign_list'),
    path('add_vote/<int:campaign_name_id>/', add_vote, name='add_vote'),
    path('check_result/<int:campaign_name_id>/', check_result, name='check_result'),
    path('stv_calculator/', stv_calculator, name='stv_calculator'),
]
