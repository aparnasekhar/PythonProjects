from django.contrib import admin
from .models import Campaign, Donation, Comment, Backer, Message

# Register your models here.
admin.site.register(Campaign)
admin.site.register(Donation)
admin.site.register(Comment)
admin.site.register(Backer)
admin.site.register(Message)