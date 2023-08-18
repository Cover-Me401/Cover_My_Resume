from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
import openai
from dotenv import load_dotenv
import os
import PyPDF2
import openai
import json
import re
from .models import Resume
import io

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
# from templates.home imprt Form
# for path in sys.path:
#    print(path)


def open_resume(pdf_path_or_bytes):
    # Check if the input is a path or bytes object
    if isinstance(pdf_path_or_bytes, bytes):
        # Convert bytes to a file-like object
        pdf_stream = io.BytesIO(pdf_path_or_bytes)
    else:
        pdf_stream = open(pdf_path_or_bytes, 'rb')
    
    reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text



def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_contents = request.FILES['file'].read()
            resume_text = open_resume(pdf_contents)
            # Further processing can be done with the extracted resume text
            # For now, just returning the extracted text
            return HttpResponse(resume_text, content_type="text/plain")
    else:
        form = UploadPDFForm()

    return render(request, 'upload.html', {'form': form})
def upload_pdf(request):
    # print(request)
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_contents = request.FILES.get('pdf_file').read()

       # Do any processing or saving of the file as needed

        resume_text = open_resume(pdf_contents)
        stored_resume = Resume(description = resume_text)
        stored_resume.save()
    return JsonResponse({'status': 200})
    # return resume_text
        # # Pass the resume text and job description to the generate_cover_letter function
        # cover_letter = generate_cover_letter(resume_text, job_description="")
    
# HERE we need to bring in job description
# ------------------------------------------------------------
# This file scrapes a job search site for listings based on the user's selected keyword(s) and location. It takes the text it receives back and strips away any html in the text. Then it waits via async before looping through each job description, inputting the job plus user data to an openai prompt, and returning a cover letter for each job with the input information.
# poetry run python cover_me_app/glassdoorScraper/run.py
# import sys
# sys.path.append('/Users/danielquinn/School/401-codefellows/cover-me-final/CoverMeResume/resume_reader')
# for path in sys.path:
#    print(path)


def get_descriptions():
  descriptions = []
  with open('cover_me_app/indeed_scraper/results/jobs.json', 'r') as file:
    job_details = file.read()
    parsed_job_details = json.loads(job_details)
    length_jobs = len(parsed_job_details)
  for i in range(length_jobs):
    description = parsed_job_details[i]['description']
    descriptions.append(description)
  return descriptions[:2]  # Return only the first 2 descriptions

def striphtml(json_details):
  p = re.compile(r'<.*?>')
  return p.sub('', json_details)

async def gpt():
    load_dotenv()
    openai.api_key = os.environ['OPENAI_API_KEY']

    resume_filename = input('Enter your resume filename: ')  # Get the resume filename from the user
    user_experience = open_resume(resume_filename)  # Get the work experience from the resume

    descriptions = get_descriptions()

    for idx, description in enumerate(descriptions):
        cover_letter = generate_cover_letter(user_experience, description)  # Generate the cover letter
        print(f'Cover Letter {idx+1}: {cover_letter}\n\n')
# ------------------------------------------------------------
# job_title and location
def generate_cover_letter(resume_text, job_description=""):
    prompt = "Write a cover letter for the job with the following information:\n\nResume Text: {}\n\nJob Description: {}".format(
        resume_text, job_description
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        top_p=0.9,
    )
    return response.choices[0].text.strip()


# down here we want to run the functions that make the magic happen


# generate_cover_letter(resume_text, job_description)


# def generate_cover_letter(resume_text, job_description):
#     prompt = "Write a cover letter for the job with the following information:\n\nResume Text: {}\n\nJob Description: {}".format(
#         resume_text, job_description
#     )

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=500,
#         temperature=0.7,
#         top_p=0.9,
#     )

#     return response.choices[0].text.strip()