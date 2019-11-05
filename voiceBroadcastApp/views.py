from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from urllib.parse import parse_qs

# Create your views here.
from voiceBroadcastApp.forms import PhoneBookForm, CampaignForm, ContactForm, CampaignForm2
from voiceBroadcastApp.models import Campaign, Contact, PhoneBook, Call


def home(request):
    return render(request, 'base/base.html')


def phonebooks(request):
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
        form = CampaignForm(user=request.user)
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

@csrf_exempt
def status(request):
    if request.method == 'POST':
        print(request.body)
        status = parse_qs(request.body.decode('UTF-8'))
        call = Call.objects.get(call_sid=status['CallSid'][0])
        call.duration=status['CallDuration'][0]
        call.save()
        print(status['CallDuration'][0])
        return HttpResponse('OK', 200)

def start_campaign(request, id):
    campaign = Campaign.objects.get(id=id)
    campaign.status = 'started'
    campaign.started_date = datetime.now()
    campaign.save()
    call_phonebook(request, campaign)
    return HttpResponseRedirect("/campaign/")



def call_phonebook(request, campaign):
    phone_book_id = campaign.phone_book_id
    contact_all = PhoneBook.objects.get(id=phone_book_id).contact_set.all()
    print(contact_all)
    for contact in contact_all:
        account_sid = 'ACed188efc96ad178ff5f8d8328dacb015'
        auth_token = '3330163189523e230405811a97135c82'
        print(contact.phone_number)
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            status_callback='https://7f92a7e8.ngrok.io/status/',
            status_callback_event=['completed'],
            status_callback_method='POST',
            url='http://demo.twilio.com/docs/voice.xml',
            to='+91' + str(contact.phone_number),
            from_='+19714071428'
        )
        callDb = Call(agent=request.user, campaign_id=campaign, call_sid=call.sid, duration=0, contact=contact, cost=0)
        callDb.save()
        print(call.sid)
