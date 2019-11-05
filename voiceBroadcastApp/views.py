from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers



# Create your views here.
from voiceBroadcastApp.forms import PhoneBookForm, CampaignForm, ContactForm
from voiceBroadcastApp.models import Campaign


def home(request):
    return render(request, 'base/base.html')


def  phonebooks(request):
    return render(request, 'voiceBroadcastApp/phonebooks.html')


def create_phone_book(request):
    if request.method == 'POST':
        form = PhoneBookForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('#')
    else:
        form = PhoneBookForm()
    return render(request, 'voiceBroadcastApp/create_phone_book.html', {'form': form})


def contacts(request):
    print("hello world")
    return render(request, 'voiceBroadcastApp/contacts.html')


def add_contact(request):
    print("hello world tarun")
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('#')
    else:
        form = ContactForm()
    return render(request, 'voiceBroadcastApp/add_new_contact.html', {'form': form})


def campaign(request):
    campaigns = Campaign.objects.filter(agent=request.user)
    return render(request, 'voiceBroadcastApp/campaign.html', {'campaigns': campaigns})

def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES or None)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            return HttpResponseRedirect('#')
    else:
        form = CampaignForm()
    return render(request, 'voiceBroadcastApp/add_campaign.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("../")
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def start_campaign(request, id):
    print("tarun")
    return HttpResponseRedirect("/campaign/")
