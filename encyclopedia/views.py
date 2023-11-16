from django.shortcuts import render
from markdown2 import Markdown 
from . import util


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