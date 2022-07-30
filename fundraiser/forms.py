from django.forms import ModelForm, Textarea, DateInput, TextInput, DateField
from .models import *
from django import forms

class createFundraiserForm(ModelForm):
   
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'amount_needed', 'category', 'end_date']
        widgets = {
            'title' :  TextInput(attrs={ 'class' : 'form-control'}),
            'amount_needed' : TextInput(attrs={ 'class' : 'form-control'}),
            'category' : TextInput(attrs={ 'class' : 'form-control'}),
            'end_date' : forms.DateInput(attrs={ 'class' : 'form-control datepicker'}),
            'description': Textarea(attrs={'class' : 'form-control', 'cols': 40, 'rows': 6}),   
        }

class donationForm(ModelForm):

    class Meta:
        model = Donation
        fields = ['donation']
        widgets = {
            'donation' : TextInput(attrs={ 'class' : 'form-control'}),
        }

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment' : Textarea(attrs={'class' : 'form-control', 'cols': 40, 'rows': 6}),   
        }