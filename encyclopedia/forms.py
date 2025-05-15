from django import forms 

class CreateEntry(forms.Form):
    title = forms.CharField(max_length=50, min_length=1, label="Title")
    content = forms.CharField(min_length=1, label="Content", widget=forms.Textarea)

class SearchEntry(forms.Form):
    search = forms.CharField(max_length=50, min_length=1)
    
class EditEntry(forms.Form):
     content = forms.CharField(min_length=1, label="Content", widget=forms.Textarea)