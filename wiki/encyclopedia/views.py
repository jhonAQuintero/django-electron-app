from django.shortcuts import render, HttpResponse
from django import forms
from . import util

class search_form(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class create_form(forms.Form):
    title =  forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'name':'body', 'rows': 8, 'cols': 3}))
    

def index(request):
    form = search_form()
    
    return render(request, "encyclopedia/index.html", {
        'entries': 'util.list_entries()',
        'form' : form
    })


def entry_page(request, title):
    form = search_form()
    entry = util.get_entry(title)
    if entry:
        return render(request, template_name="encyclopedia/page.html", context={'form': form, 'title': title, 'entry': entry})
    else:
        return render(request, template_name="encyclopedia/page.html", context={'form': form, 'title': title, 'entry': entry})


def search_page(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entry = util.get_entry(title)
            if entry:
                return render(request, template_name="encyclopedia/page.html", context={'form': form, 'title': title, 'entry': entry})
            else:
                entries_search = []
                for item in util.list_entries():
                    if item.lower().find(title.lower()) != -1:
                        entries_search.append(item)
                print(entries_search)
                return render(request, template_name="encyclopedia/page.html", context={'form': form, 'title': title, 'entry': entry, 'entries_search': entries_search})
    else:
        form = search_form()
        return render(request, 'encyclopedia/index.html', {'entries': util.list_entries(),'form' : form})
    

def form_create_page(request):
    if request.method == 'POST':
        form = search_form()
        form_page = create_form(request.POST)
        if form.is_valid():
            title = request.post['title']
            body = request.post['body']
            return render(request, template_name="encyclopedia/page.html", context={'form': form, 'title': title, 'entry': body})
    else:
        form = search_form()
        form_page = create_form()
        return render(request, 'encyclopedia/handlepage.html', {'entries': util.list_entries(),'form' : form, 'form_page' : form_page})
    

