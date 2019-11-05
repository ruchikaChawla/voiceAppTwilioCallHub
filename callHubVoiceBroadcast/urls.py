"""callHubVoiceBroadcast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from StatusCallback.views import index
from voiceBroadcastApp.views import home, add_contact, register, phonebooks, contacts, campaign, create_phone_book, \
    add_campaign, start_campaign, status

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('status/', status, name='status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('phonebooks/', phonebooks, name='phonebooks'),
    path('create_phone_book/', create_phone_book, name='create_phone_book'),
    path('contacts/', contacts, name='contacts'),
    path('add_contact/', add_contact, name='add_contact'),
    path('campaign/', campaign, name='campaign'),
    path('add_campaign/', add_campaign, name='add_campaign'),
    path('start_campaign/<int:id>', start_campaign, name='start_campaign')
]
