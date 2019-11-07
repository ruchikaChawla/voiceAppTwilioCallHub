from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from urllib.parse import parse_qs
from voiceBroadcastApp.forms import PhoneBookForm, CampaignForm, ContactForm, CampaignForm2, ContactForm2
from voiceBroadcastApp.models import Campaign, Contact, PhoneBook, Call


def home(request):
    return render(request, 'base/base.html')


@csrf_exempt
def voice_xml(request, id, phone_no):
    campaign_text = Campaign.objects.get(id=id).text_speech
    name = Contact.objects.get(phone_number=phone_no).first_name
    available_params = {'first_name': name}
    new_str = campaign_text.format(**available_params)
    template_var = {'msg': new_str}
    t = loader.get_template('voiceBroadcastApp/voice.xml')
    return HttpResponse(t.render(template_var), content_type='text/xml')


def phonebooks(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    phonebooks = PhoneBook.objects.filter(agent=request.user)
    return render(request, 'voiceBroadcastApp/phonebooks.html', {'phonebooks': phonebooks})


def create_phone_book(request):
    if request.method == 'POST':
        form = PhoneBookForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            return HttpResponseRedirect('../phonebooks')
    else:
        form = PhoneBookForm()
    return render(request, 'voiceBroadcastApp/create_phone_book.html', {'form': form})


def contacts(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    contacts = Contact.objects.filter(agent=request.user)
    return render(request, 'voiceBroadcastApp/contacts.html', {'contacts': contacts})


def view_phonebook_contacts(request, id):
    phonebook = PhoneBook.objects.get(id=id)
    contacts = phonebook.contact_set.all()
    return render(request, 'voiceBroadcastApp/contacts.html', {'contacts': contacts, 'phonebook_name': phonebook, 'id': id})


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm2(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.agent = request.user
            newForm.save()
            form.save_m2m()
            return HttpResponseRedirect('#')
    else:
        form = ContactForm(user=request.user)
    return render(request, 'voiceBroadcastApp/add_new_contact.html', {'form': form})


def campaign(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    campaigns = Campaign.objects.filter(agent=request.user)
    for campaign in campaigns:
        calls = campaign.call_set.all()
        completed = True
        for call in calls:
            if not call.completed:
                completed = False
        if calls.count() > 0:
            if completed:
                campaign.status = 'completed'
        campaign.save()
    return render(request, 'voiceBroadcastApp/campaign.html', {'campaigns': campaigns})


def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm2(request.POST)
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
        status = parse_qs(request.body.decode('UTF-8'))
        per_min_cost = 2
        total_cost = (per_min_cost * int(status['CallDuration'][0])) / 60
        call = Call.objects.get(call_sid=status['CallSid'][0])
        call.duration = status['CallDuration'][0]
        call.completed = True
        call.cost = total_cost
        call.save()
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
            status_callback='http://ead3d853.ngrok.ioF/status/',
            status_callback_event=['completed'],
            status_callback_method='POST',
            url='http://ead3d853.ngrok.io/xml/' + str(campaign.id) + '/' + str(contact.phone_number) + '/voice.xml/',
            to='+91' + str(contact.phone_number),
            from_='+19714071428'
        )
        callDb = Call(agent=request.user, caller_id='+19714071428', call_sid=call.sid, duration=0,
                      contact=contact, cost=0, campaign=campaign)
        callDb.save()


def call_history(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    calls = Call.objects.filter(agent=request.user)
    return render(request, 'voiceBroadcastApp/call_history.html', {'calls': calls})


def campaign_call_history(request, id):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    calls = Campaign.objects.get(id=id).call_set.all()
    call_cost = 0
    for call in calls:
        call_cost = call_cost + call.cost
    return render(request, 'voiceBroadcastApp/call_history.html', {'calls': calls, 'call_cost': call_cost, 'id': id})


def edit_contacts(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == 'POST':
        contactForm = ContactForm2(request.POST, instance=contact)
        if contactForm.is_valid():
            newForm = contactForm.save(commit=False)
            newForm.save()
            contactForm.save_m2m()
            return HttpResponseRedirect("/contacts/")
    else:
        contactForm = ContactForm2(instance=contact)
    return render(request, 'voiceBroadcastApp/edit_contacts.html', {'form': contactForm})
