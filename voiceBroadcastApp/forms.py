import kwargs as kwargs
from django.forms import ModelForm

from voiceBroadcastApp.models import Contact, PhoneBook, Campaign


class ContactForm(ModelForm):
    def __init__(self, *args, **kwrgs):
        self.user = kwrgs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwrgs)
        self.fields['phone_book'].queryset = PhoneBook.objects.filter(agent=self.user)

    class Meta:
        model = Contact
        fields = ['first_name',
                  'last_name',
                  'phone_number',
                  'phone_book']


class ContactForm2(ModelForm):
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
    def __init__(self, *args, **kwrgs):
        self.user = kwrgs.pop('user', None)
        super(CampaignForm, self).__init__(*args, **kwrgs)
        self.fields['phone_book'].queryset = PhoneBook.objects.filter(agent=self.user)

    class Meta:
        model = Campaign
        fields = ['name', 'text_speech', 'phone_book']


class CampaignForm2(ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'text_speech', 'phone_book']
