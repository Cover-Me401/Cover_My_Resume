# import PyPDF2
# import sys
# # from templates.home imprt Form
# # for path in sys.path:
# #    print(path)

# def open_resume(pdf_path):
#     # Creating a pdf reader object
#     reader = PyPDF2.PdfReader(pdf_path)
    
#     # Initializing an empty string to store extracted text
#     extracted_text = ""
    
#     # Loop through each page and extract text
#     for page in reader.pages:
#         extracted_text += page.extract_text()
    
#     return extracted_text # RESUME INFORMATION, VERY IMPORTANT

# if __name__ == "__main__":
#     pdf_path = "cover_me_app/resumes/DansResume.pdf"
#     resume_text = open_resume(pdf_path)
#     print(resume_text)
