from django.shortcuts import render
import markdown2
from django import forms
from django.urls import reverse
from . import util
from django.http import HttpResponseRedirect
import secrets
import re

class newEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    md = markdown2.Markdown()
    entry_page = util.get_entry(entry)
    if entry_page is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(entry_page),
            "entryTitle": entry,
            "existing": True
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "existing": False
        })

def newEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form" : form,
                    "existing": True,
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
            "form" : form
            })
    else:
        return render(request,"encyclopedia/newEntry.html", {
            "form" : newEntryForm()
            })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))

def search(request):
        query = request.GET.get('q')
        if util.get_entry(query) is not None:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
                "title": f'"{query}" search results',
                "heading": f'Search Results for "{query}"'
            })

def edit(request,entry):
    entrypage = util.get_entry(entry)
    form = newEntryForm()
    form.fields["title"].initial = entry
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = entrypage
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/newEntry.html", {
        "form": form,
        "edit": form.fields["edit"].initial,
        "entryTitle": form.fields["title"].initial
    })