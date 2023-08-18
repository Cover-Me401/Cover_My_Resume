import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
# LinkedIn is one of the STRONGEST blockers of scraping databases. This code returns enough for a prompt and includes the link. Link can be accessed but may result in an IP ban if you try too many times. 
# USE AT YOUR OWN RISK IF YOU CHANGE TO READ THE URL LINKS.
def linkedin_jobs_scraper(keywords, location, page_number):
  """Scrape job listings from LinkedIn."""
  url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&geoId={103644278}&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=2931031787&position=1&pageNum={page_number}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  jobs = []
  for job in soup.find_all("li"):
    job_title = job.find("h3").text.strip()
    company = job.find("h4").text.strip()
    location = job.find("span").text.strip()
    link = job.find("a").get("href")

    jobs.append({
      "Title": job_title,
      "Company": company,
      "Location": location,
      "Link": link,
    })

  return jobs

def main():
  """Scrape job listings from LinkedIn."""
  keywords = input("Enter keywords: ")
  location = input("Enter location: ")

  jobs = []
  for page_number in range(0, 1000, 25):
    try:
      jobs.extend(linkedin_jobs_scraper(keywords, location, page_number))
      
      # Break the loop if we have 20 or more jobs
      if len(jobs) >= 20:
        jobs = jobs[:20]  # Only take the first 20 jobs
        break
    except requests.exceptions.RequestException as e:
      print(f"Error scraping page {page_number}: {e}")

  if not jobs:
    print("No job listings found.")
  else:
    jobs_json = {"jobs": jobs}
    # Create the results folder if it does not exist
    output = Path(__file__).parent / "results"
    output.mkdir(parents=True, exist_ok=True)

    # Save the job listings to the results folder
    with open(output / "linkedin_jobs.json", "w") as f:
      f.write(json.dumps(jobs_json))

if __name__ == "__main__":
  main()