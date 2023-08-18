from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

class Coverletter(models.Model):
  """_summary_

  Args:
      models (_type_): _description_

  Returns:
      _type_: _description_
  """
  # upload = models.ImageField(upload_to='images/')
  title = models.CharField(max_length=250)
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  description = models.TextField(default='coverletter description or info')
  
  def __str__(self):
    return str(self.pk, self.title)
    """_summary_

    Returns:
        _type_: _description_
    """

  def get_absolute_url(self):
    return reverse('coverletter_detail', kwargs={'pk': self.id})



class Job(models.Model):
    title = models.CharField(max_length=250, default="Default Title")

    location = models.CharField(max_length=64, default='unknown', null=True, blank=True)


    description = models.TextField(default='job description or info')

    def __str__(self):
        return str(self.pk) + " - " + self.title

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'pk': self.id})

  
class Resume(models.Model):
  description = models.TextField(default='resume_text')
  file = models.FileField()