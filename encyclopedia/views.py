from django import forms
from django.shortcuts import render
import markdown2
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from random import choice

current_entries = util.list_entries()

class newEntryForm(forms.Form):
	title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}))
	body = forms.CharField(label="Body", widget=forms.Textarea(attrs={'class': 'form-control w-75'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def displayEntry(request, title):
	content = util.get_entry(title)
	if content:
		html = markdown2.markdown(content)
		return render(request, "encyclopedia/displayEntry.html", {
				"entry": html, 
				"title": title,
			})
	return render(request, "encyclopedia/error.html", {
			"title": title
		})

def search(request):
	query = request.GET.get('q', '').lower().capitalize()
	if util.get_entry(query):
		return HttpResponseRedirect(reverse("wiki:title", kwargs={'title': query}))
	matches = [entry for entry in current_entries if query.lower() in entry.lower()]
	return render(request, "encyclopedia/search.html", {
			"matches": matches, 
			"results": len(matches),
			"query": query,
		})

def new(request):
	if request.method == "POST":
		form = newEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			md = form.cleaned_data["body"]
			util.save_entry(title, md)
			return HttpResponseRedirect(reverse("wiki:title", kwargs={'title': title}))

	form = newEntryForm()
	
	if request.path == "/wiki/edit":
		title = util.get_edit(request.META.get('HTTP_REFERER'))
		md = util.get_entry(title)
		form["title"].initial = title
		form["body"].initial = md
	return render(request, "encyclopedia/new.html", {
			"form": form
		})

def random(request):
	title = choice(current_entries)
	return HttpResponseRedirect(reverse("wiki:title", kwargs={'title': title}))



