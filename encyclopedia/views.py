from django.shortcuts import render, redirect
from markdown2 import Markdown 
from . import util
# from .forms import SearchForm
from django.http import HttpResponseNotFound

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    markdown = Markdown()
    entry = util.get_entry(name)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": name,
            "body": markdown.convert(entry)
        }) 
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    markdown = Markdown()
    search_query = request.GET.get("q").lower()
    all_pages = util.list_entries()
    result = util.search(all_pages, search_query)
    
    if result[0] == True:
        entry = util.get_entry(result[1][0])
        return render(request,"encyclopedia/entry.html", {
            "entry": result[1][0],
            "body": markdown.convert(entry)
        })
    else:
        return render(request,"encyclopedia/search.html", {
            "search_results": result[1]
        })
        
