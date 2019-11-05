from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from twilio.rest import Client



# Create your views here.
from voiceBroadcastApp.forms import PhoneBookForm, CampaignForm, ContactForm, CampaignForm2
from voiceBroadcastApp.models import Campaign, Contact, PhoneBook


def home(request):
    return render(request, 'base/base.html')


def  phonebooks(request):
    return render(request, 'voiceBroadcastApp/phonebooks.html')


def create_phone_book(request):
    if request.method == 'POST':
        form = PhoneBookForm(request.POST, request.FILES or None)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            return HttpResponseRedirect('#')
    else:
        form = PhoneBookForm()
    return render(request, 'voiceBroadcastApp/create_phone_book.html', {'form': form})


def contacts(request):
    return render(request, 'voiceBroadcastApp/contacts.html')


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES or None)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            return HttpResponseRedirect('#')
    else:
        form = ContactForm()
    return render(request, 'voiceBroadcastApp/add_new_contact.html', {'form': form})


def campaign(request):
    campaigns = Campaign.objects.filter(agent=request.user)
    return render(request, 'voiceBroadcastApp/campaign.html', {'campaigns': campaigns})


def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm2(request.POST, request.FILES or None)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            return HttpResponseRedirect('#')
    else:
        form = CampaignForm(user = request.user)
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
    campaign = Campaign.objects.get(id=id)
    campaign.status = 'started'
    campaign.started_date = datetime.now()
    campaign.save()
    call_phonebook(campaign.phone_book_id)
    return HttpResponseRedirect("/campaign/")


def call_phonebook(phone_book_id):
    contact_all = PhoneBook.objects.get(id=phone_book_id).contact_set.all()
    print(contact_all)
    for contact in contact_all:
        account_sid = 'ACed188efc96ad178ff5f8d8328dacb015'
        auth_token = '3330163189523e230405811a97135c82'
        print(contact.phone_number)
        client = Client(account_sid, auth_token)
        #call = client.calls.create(
           # status_callback='http://ruchika94chawla.pythonanywhere.com/',
           # status_callback_event=['initiated', 'answered', 'completed'],
            #status_callback_method='POST',
            ##url='http://demo.twilio.com/docs/voice.xml',
            #to='+91'+str(contact.phone_number),
            #from_='+19714071428'
        #)
