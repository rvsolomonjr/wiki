from django.shortcuts import render, redirect
import markdown2
from .forms import EditEntry, CreateEntry
from . import util
import random


def create(request):
    entry = CreateEntry()
    return render(request, "encyclopedia/create.html", {
     "form": entry   
    })

def edit(request, entry):
    form = EditEntry()
    content = util.get_entry(entry)  
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "form": form,
        "content": content     
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q', '').lower()  # Get and lowercase the query
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query == entry.lower():
                return redirect(f'/wiki/{entry}')  # Redirect to exact match
            elif query in entry.lower():
                results.append(entry)
        if results:
            return render(request, "encyclopedia/search.html", {"results": results, "title": query})
        else:
            return render(request, "encyclopedia/not_found.html", {"entry": query})
    else:
        return redirect("index")  # Redirect to home if not a POST request

def show(request, entry):
    article = util.get_entry(entry)
    if article is None:
        return render(request, "encyclopedia/not_found.html", {"entry": entry, "title": entry})
    else:
        article_html = markdown2.markdown(article)
        return render(request, "encyclopedia/show.html", {"entry": article_html, "title": entry})


def save(request, entry):
    if request.method == 'POST':
        title = request.POST["title"]
        for entri in util.list_entries():
            if title.lower() == entri.lower():
                return render(request, "encyclopedia/alreadyexists.html", {"entry": entri})
        content = request.POST["content"]
        util.save_entry(title, content)
        return show(request, title)


def save_edited(request, entry):  # 'entry' is the *old* title
    if request.method == 'POST':
        new_title = request.POST["title"]
        content = request.POST["content"]

        if new_title.lower() != entry.lower():  # Title has changed
            util.delete_entry(entry)  # Delete the old entry
            util.save_entry(new_title, content)  # Save with the new title
            return show(request, new_title)  # Redirect to the newly titled page
        else:
            util.save_entry(entry, content)  # Save with the same title
            return show(request, entry)  # Redirect to the page


def randomize(request):
    page = random.choice(util.list_entries())
    return show(request, page)