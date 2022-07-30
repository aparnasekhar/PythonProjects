from django.forms import ModelForm, Textarea, IntegerField, TextInput
from .models import *
from django import forms

class createListForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'starting_bid', 'image_url', 'category', 'description' ]
        widgets = {
            'title' :  TextInput(attrs={ 'class' : 'form-control'}),
            'starting_bid' : TextInput(attrs={ 'class' : 'form-control'}),
             'image_url' : TextInput(attrs={ 'class' : 'form-control'}),
             'category' : TextInput(attrs={ 'class' : 'form-control'}),
            'description': Textarea(attrs={'class' : 'form-control', 'cols': 40, 'rows': 6}),
        }

#class bidForm(ModelForm):
   # class Meta:
       # model = Bid
        #fields = ['bid_price']
       