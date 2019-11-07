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

from voiceBroadcastApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('status/', views.status, name='status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('phonebooks/', views.phonebooks, name='phonebooks'),
    path('create_phone_book/', views.create_phone_book, name='create_phone_book'),
    path('contacts/', views.contacts, name='contacts'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('campaign/', views.campaign, name='campaign'),
    path('add_campaign/', views.add_campaign, name='add_campaign'),
    path('call_history/', views.call_history, name='call_history'),
    path('xml/<int:id>/<int:phone_no>/voice.xml/', views.voice_xml, name='voice_xml'),
    path('start_campaign/<int:id>', views.start_campaign, name='start_campaign'),
    path('campaign_call_history/<int:id>', views.campaign_call_history, name='campaign_call_history'),
    path('view_phonebook_contacts/<int:id>', views.view_phonebook_contacts, name='view_phonebook_contacts'),
    path('edit_contacts/<int:id>', views.edit_contacts, name='edit_contacts')
]
