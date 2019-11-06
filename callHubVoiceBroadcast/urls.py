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

from voiceBroadcastApp.views import home, add_contact, register, phonebooks, contacts, campaign, create_phone_book, \
    add_campaign, start_campaign, status, call_history, voice_xml, campaign_call_history, view_phonebook_contacts, edit_contacts

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
    path('call_history/', call_history, name='call_history'),
    path('xml/<int:id>/<int:phone_no>/voice.xml/', voice_xml, name='voice_xml'),
    path('start_campaign/<int:id>', start_campaign, name='start_campaign'),
    path('campaign_call_history/<int:id>', campaign_call_history, name='campaign_call_history'),
    path('view_phonebook_contacts/<int:id>', view_phonebook_contacts, name='view_phonebook_contacts'),
    path('edit_contacts/<int:id>', edit_contacts, name='edit_contacts')
]
