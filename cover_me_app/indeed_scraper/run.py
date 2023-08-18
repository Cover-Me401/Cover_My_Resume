# This file specifies that the scraper should identify and retrieve job information based on each job's ID key. 

# https://github.com/scrapfly/scrapfly-scrapers/tree/main/indeed-scraper
# To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
# $ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
# poetry run python Docker/modules/indeed_scraper/run.py

# import asyncio-NEEDED FOR TESTING
import json
from pathlib import Path
from .indeed import BASE_CONFIG
import cover_me_app.indeed_scraper.indeed as indeed
import asyncio

# Change this to your absolute path
output = Path(__file__).parent / "results"
output.mkdir(parents=True, exist_ok=True)

# UNCOMMENT THESE FOR TESTING THIS FILE
# job_specification = input('Enter job role: ')
# job_specification = job_specification.replace(" ", "+")
# location = input('Enter a location: ')

async def run(job_specification, location):
  # enable scrapfly cache for basic use
  BASE_CONFIG["cache"] = True

  url = f"https://www.indeed.com/jobs?q={job_specification}&l={location}"
  result_search = await indeed.scrape_search(url, max_results=10)
  output.joinpath("search.json").write_text(json.dumps(result_search, indent=2, ensure_ascii=False))
  
  # Extract job keys from the search results
  job_keys = [job['jobkey'] for job in result_search]
      
  # Save the extracted job keys to a list
  job_keys_path = output.joinpath("job_keys.txt")
  job_keys_path.write_text('\n'.join(job_keys))
  
  result_jobs = await indeed.scrape_jobs(job_keys)
  output.joinpath("jobs.json").write_text(json.dumps(result_jobs, indent=2, ensure_ascii=False))

# UNCOMMENT THESE FOR TESTING THIS FILE
# if __name__ == "__main__":
#   asyncio.run(run(job_specification, location))