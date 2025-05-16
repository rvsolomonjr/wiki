from django.shortcuts import render, redirect
import markdown2
from . import util
from .forms import EditEntry, CreateEntry, SearchEntry
import random

def edit(request, entry):
    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/not_found.html", {"entry": entry})
    
    form = EditEntry()
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "content": content,
        "form": form
    })


def create(request):
    """Display the create page with a blank form"""
    form = CreateEntry()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })


def create_save(request):
    """Handle saving newly created entries"""
    if request.method == 'POST':
        form = CreateEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            # Check if entry already exists
            for entri in util.list_entries():
                if title.lower() == entri.lower():
                    return render(request, "encyclopedia/alreadyexists.html", {"entry": entri})
            
            # Prepend title as heading if not already present
            if not content.startswith(f"# {title}"):
                content = f"# {title}\n\n{content}"
            
            # Save the entry and redirect to its page
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
        else:
            # If form is invalid, redisplay with error messages
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    
    # Redirect to create page if someone tries to access via GET
    return redirect('create')


def index(request):
    if request.method == 'POST':
        if request.POST.get('q') == None:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        else:
            entry = str(request.POST.get('q'))
            list_entries = util.list_entries()
            results = []
            
            # Check for exact match first (case-insensitive)
            for i in list_entries:
                if entry.lower() == i.lower():
                    print(f'found {i}')
                    return redirect(f'/wiki/{i}')
                elif entry.lower() in i.lower():
                    results.append(i)
            
            # If no exact match but we have partial matches
            if results:
                return render(request, "encyclopedia/search.html", {"results": results, "title": entry})
            else:
                return render(request, "encyclopedia/not_found.html", {"entry": entry})

    # If not a POST request, just show the index
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show(request, entry):
    if request.method == "POST":
        query = request.POST.get('q')
        if query is None:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        else:
            entri = str(query)
            list_entries = util.list_entries()
            results = []
            
            # Check for exact match first (case-insensitive)
            for i in list_entries:
                if entri.lower() == i.lower():
                    print(f'found {i}')
                    return redirect(f'/wiki/{i}')
                elif entri.lower() in i.lower():
                    results.append(i)
            
            # If no matches found
            if not results:
                return render(request, "encyclopedia/not_found.html", {"entry": entri})
            
            # If we have partial matches
            return render(request, "encyclopedia/search.html", {"results": results, "title": entri})
    
    # If not a POST request, show the requested entry
    article = util.get_entry(entry)
    print(f'article: {entry}')
    if article is None:
        return render(request, "encyclopedia/not_found.html", {"entry": entry, "title": entry})
    else:
        article_html = markdown2.markdown(article)
        return render(request, "encyclopedia/show.html", {
            "entry": article_html,
            "title": entry
        })


def save(request, entry):
    """Handle saving edited entries"""
    if request.method == 'POST':
        title = request.POST["title"]
        for entri in util.list_entries():
            if title.lower() == entri.lower() and title.lower() != entry.lower():
                return render(request, "encyclopedia/alreadyexists.html", {"entry": entri})
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect(f'/wiki/{title}')


def save_edited(request, entry):
    if request.method == 'POST':
        title = entry
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect(f'/wiki/{title}')


def randomize(request):
    page = random.choice(util.list_entries())
    return redirect(f'/wiki/{page}')


def delete(request, title):
    """
    Handles the deletion of an encyclopedia entry.
    """
    util.delete_entry(title)
    return redirect('index')  # Redirect to the index page after deletion