from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse 
from .models import Coverletter, Job
from rest_framework.generics import (
  ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from .serializers import CoverletterSerializer
from .models import Coverletter
from .permissions import IsOwnerOrReadOnly 
from django.http import HttpResponse
from .cover_letter_generator import upload_pdf
from .indeed_scraper.run import run
import asyncio

from django.shortcuts import render, redirect
from .cover_letter_generator import get_descriptions  # Import the function that generates the descriptions

# Coverletter Views

class CoverletterListView(LoginRequiredMixin, ListView):
  template_name = 'coverletters/coverletter_list.html'
  model = Coverletter
  context_object_name = 'coverletters'
    
class CoverletterDetailView(LoginRequiredMixin, DetailView):
  template_name = 'coverletters/coverletter_detail.html'
  model = Coverletter

class CoverletterCreateView(LoginRequiredMixin, CreateView):
  template_name = 'coverletters/coverletter_create.html'
  model = Coverletter
  fields = ('title', 'owner', 'description')
  
class CoverletterUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'coverletters/coverletter_update.html'
  model = Coverletter
  fields = '__all__'
  
class CoverletterDeleteView(LoginRequiredMixin, DeleteView):
  template_name = 'coverletters/coverletter_delete.html'
  model = Coverletter
  success_url = reverse_lazy('coverletter_list')


# Job Views

class JobListView(LoginRequiredMixin, ListView):
  template_name = 'jobs/job_list.html'
  model = Job
  context_object_name = 'jobs'
    
class JobDetailView(LoginRequiredMixin, DetailView):
  template_name = 'jobs/job_detail.html'
  model = Job

class JobCreateView(LoginRequiredMixin, CreateView):
  template_name = 'jobs/job_create.html'
  model = Job
  fields = ('__all__')
  
class JobUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'jobs/job_update.html'
  model = Job
  fields = '__all__'
  
class JobDeleteView(LoginRequiredMixin, DeleteView):
  template_name = 'jobs/job_delete.html'
  model = Job
  success_url = reverse_lazy('job_list')

class JobQueryView(LoginRequiredMixin, CreateView):
  template_name = 'jobs/job_query.html'
  model = Job
  fields = '__all__'

  def form_valid(self, form):
    job_title = form.cleaned_data['job_title']
    location = form.cleaned_data['location']
    
    # Run the scraper
    asyncio.run(run(job_title, location))  # Uncomment this if you want to run the scraper
    # For the purpose of this example, I'm commenting out the scraper call.

    # If you want to save the scraped job listings to the database, you can do so here.
    # For now, I'm skipping that part.

    # Redirect to the results page
    return redirect(reverse('job_list'))
  
def uploadPDFView(request):
    print(dict(request.POST.items()))
    if request.method == 'POST':
      upload_pdf(request)
    print("uploadPDFView")
    return HttpResponse(status=201)



def job_query(request):
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        job_location = request.POST.get('location')
        
        # This is a placeholder for the logic to retrieve job information from the database
        # Modify this part based on the actual DB structure and logic
        job_info = Job.objects.filter(title=job_title, location=job_location).first()
        
        # Execute cover_letter_generator.py (or any relevant logic)
        cover_letter = get_descriptions()  # This is a placeholder, update with the actual logic
        
        # Save the cover letter (you might want to save it to the Coverletter model or elsewhere)
        cover_letter_model = Coverletter(description=cover_letter, owner=request.user)


        cover_letter_model.save()
        
        # Redirect to scraper_results page
        # return redirect(reverse('scraper_results'))
        return redirect(reverse('success', args=[cover_letter_model.id]))
    
    descriptions = get_descriptions()  # Keep the existing logic to get the job descriptions
    return render(request, 'jobs/job_query.html', {'descriptions': descriptions})

def job_query_view(request):
    if request.method == 'POST':
      job_title = request.POST.get('job_title')
      location = request.POST.get('location')
      
      asyncio.run(run(job_title, location))  # Run the scraper
      
      return redirect('success url or results page')
    return render(request, 'jobs/job_query.html')

def scraperResult(request):
    print(dict(request.POST.items()))
    if request.method == 'POST':
      scraper_Results(request)
    print("uploadPDFView")
    return HttpResponse(status=201)
from django.shortcuts import render, redirect
from .indeed_scraper.indeed import fetch_indeed_listings
from .cover_letter_generator import open_resume, generate_cover_letter
from .models import Resume
from .forms import JobSearchForm

def job_search(request):
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data['job_title']
            location = form.cleaned_data['location']
            
            # Fetch job descriptions using the scraper
            job_descriptions = fetch_indeed_listings(job_title, location)
            
            # For demonstration purposes, we'll use the first job description
            job_description = job_descriptions[0] if job_descriptions else ""
            
            # Extract user's resume from the database
            # Assuming the user has only one resume stored
            resume_obj = Resume.objects.first()
            resume_text = open_resume(resume_obj.file.path)
            
            # Generate the cover letter
            cover_letter = generate_cover_letter(resume_text, job_description)
            
            return render(request, 'cover_letter_result.html', {'cover_letter': cover_letter})

    else:
        form = JobSearchForm()

    return render(request, 'job_search.html', {'form': form})


def success_view(request, coverletter_id):
    return render(request, 'success.html', {'coverletter_id': coverletter_id})
