# CoverMeResume

## Authors

- Logan Reese
- Sarah Glass
- Anthony Sinitsa
- Daniel Quinn

## 🚀 Features

### Frontend

**What is the vision of this product?**
We will create an app that will include a React frontend page and a Django backend with database that will allow users to search for jobs by keyword, scrape job information from indeed.com, save jobs they are interested in, and run the job's data along with their own resume through AI to produce a sample cover letter for that job.

**What pain point does this project solve?**
Helps users find relevant and recent job listings in the tech industry, select listings they like, and then prompt AI to process the listing's data to produce a sample cover letter for the given job posting.

**Why should we care about your product?**
People looking for work in the tech industry should care about this product because it will allow users to more efficiently browse, filter, and apply for recently posted relevant jobs.

### Backend

This CLI app contains a web scraper from job search site indeed.com. The app collects data for job listings in the tech industry such as company name, skills, education level, salary detail, etc. and then allows users to search for jobs by keyword and location. The code runs a selected job's data along with the user's resume (uploaded via filepath) through AI to produce a sample cover letter tailored to the user, specifically for that job.

This program helps users find relevant and recent job listings in the tech industry, select listings they like, and prompt AI to process the listing's data to produce a sample cover letter for the given job posting.

## Blueprints

[Blueprints](images/README.md)

## 📖 Installation

```
$ python -m venv .venv

$ source .venv/bin/activate

(.venv) $ pip install -r requirements.txt
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py runserver

# Load the site at http://127.0.0.1:8000
```

## Next Steps

## 🤝 Contributing

[djangox template](https://github.com/wsvincent/djangox)

[CoverMe midterm project](https://github.com/Cover-Me401/Cover_Me)

[scrapflyIndeed](https://github.com/scrapfly/scrapfly-scrapers/blob/main/indeed-scraper/README.md)

[scrapflyGlassdoor](https://github.com/scrapfly/scrapfly-scrapers/blob/main/glassdoor-scraper/README.md)

## License

[The MIT License](LICENSE)
