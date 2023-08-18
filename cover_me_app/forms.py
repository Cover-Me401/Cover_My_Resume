
from django import forms

class JobSearchForm(forms.Form):
    job_title = forms.CharField(label='Job Title', max_length=200)
    location = forms.CharField(label='Location', max_length=200)
