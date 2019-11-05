from django.forms import ModelForm

from voiceBroadcastApp.models import Contact, PhoneBook, Campaign


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name',
                  'last_name',
                  'phone_number',
                  'phone_book']


class PhoneBookForm(ModelForm):
    class Meta:
        model = PhoneBook
        fields = ['name',
                  'description']


class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ['name',
                  'text_speech',
                  'phone_book']