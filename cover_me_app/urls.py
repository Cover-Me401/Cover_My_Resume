from . import views
from django.urls import path 
from .views import CoverletterListView, CoverletterDetailView
from django.http import HttpResponse
from .views import (
  CoverletterCreateView,
  CoverletterUpdateView,
  CoverletterDeleteView,
  JobCreateView,
  JobListView,
  JobQueryView,
  JobDetailView,
  uploadPDFView,
  job_query,
)


urlpatterns = [
  path('', CoverletterListView.as_view(), name='coverletter_list'),
  path('<int:pk>/', CoverletterDetailView.as_view(), name='coverletter_detail'),
  path('create/', CoverletterCreateView.as_view(), name='coverletter_create'),
  path('<int:pk>/update/', CoverletterUpdateView.as_view(), name='coverletter_update'),
  path('<int:pk>/delete/', CoverletterDeleteView.as_view(), name='coverletter_delete'),
  path('job_query/', job_query, name='job_query'),
  path('scraper_results/', JobListView.as_view(), name='scraper_results'),
  path('scraper_results/<int:pk>', JobDetailView.as_view(), name='job_detail'),
  path('coverletter_result/<int:pk>', CoverletterDetailView.as_view(), name='coverletter_detail'),
  path('list/', CoverletterListView.as_view(), name='coverletter_list'),
  path('create_job/', JobCreateView.as_view(), name='create_job'),
  path('upload_pdf/', uploadPDFView, name='upload_pdf'),
  path('jobs/', JobListView.as_view(), name='job_list'),
  path('success/<int:coverletter_id>/', views.success_view, name='success'),

]

from .views import job_search

urlpatterns += [
    path('job_search/', job_search, name='job_search'),
]
