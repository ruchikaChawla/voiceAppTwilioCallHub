from django.contrib import admin

# Register your models here.
from voiceBroadcastApp.models import Contact, PhoneBook, Campaign, Call

admin.site.register(Contact)
admin.site.register(PhoneBook)
admin.site.register(Campaign)
admin.site.register(Call)