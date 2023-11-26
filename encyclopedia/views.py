from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django.http import HttpResponseNotFound
import random


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
        return render(request, "encyclopedia/entry.html", {
            "entry": result[1][0],
            "body": markdown.convert(entry)
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "search_results": result[1]
        })


def add(request):
    if request.method == 'GET':
        action = request.GET.get("action")
        title = request.GET.get("title")
        body = util.get_entry(title)
        return render(request, "encyclopedia/addpage.html", {
            "action": action,
            "title": title,
            "body": body
        })

    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        action = request.POST.get("action")
        entryExists = util.get_entry(title)
        markdown = Markdown()
        if entryExists is not None and action != "Save":
            return render(request, "encyclopedia/error.html")
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": title,
                "body": markdown.convert(content)
            })
    else:
        return render(request, "encyclopedia/error.html")


def random_page(request):
    entries = util.list_entries()
    random_integer = random.randint(0, len(entries)-1)
    return entry(request, entries[random_integer])