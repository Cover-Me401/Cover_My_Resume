# This file scrapes the job search site. It locates the data for up to 30 job listings based on user input and scrapes the site for job listing previews, parses jobs, from the listing page, then scrapes the individual job's page.

# https://github.com/scrapfly/scrapfly-scrapers/tree/main/indeed-scraper
# To run this scraper set env variable $SCRAPFLY_KEY with your scrapfly API key:
# $ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
import json, math, os, re
from typing import Dict, List
import urllib
from loguru import logger as log
from scrapfly import ScrapeApiResponse, ScrapeConfig, ScrapflyClient, ScrapflyScrapeError
from pathlib import Path
from dotenv import load_dotenv
import argparse
from django.conf import settings
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cover_me_project.settings')
django.setup()

api_key = settings.SCRAPFLY_API_KEY



dotenv_path = Path('../../.env')
load_dotenv(dotenv_path)
SCRAPFLY = ScrapflyClient(os.getenv('SCRAPFLY_KEY'))
BASE_CONFIG = {
  # Indeed.com requires Anti Scraping Protection bypass feature.
  "asp": True,
  "country": "US",
}

def parse_search_page(result):
  """Find hidden web data of search results in Indeed.com search page HTML"""
  data = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', result.content)
  data = json.loads(data[0])
  return {
    "results": data["metaData"]["mosaicProviderJobCardsModel"]["results"],
    "meta": data["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"],
  }


def _add_url_parameter(url, **kwargs):
  """Add or replace GET parameters in a URL"""
  url_parts = list(urllib.parse.urlparse(url))
  query = dict(urllib.parse.parse_qsl(url_parts[4]))
  query.update(kwargs)
  url_parts[4] = urllib.parse.urlencode(query)
  return urllib.parse.urlunparse(url_parts)


async def scrape_search(url: str, max_results: int = 1000) -> List[Dict]:
  """Scrape Indeed.com search for job listing previews"""
  log.info(f"scraping search: {url}")
  result_first_page = await SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG))
  data_first_page = parse_search_page(result_first_page)

  results = data_first_page["results"]
  total_results = sum(category["jobCount"] for category in data_first_page["meta"])
  # there's a page limit on indeed.com of 1000 results per search
  if total_results > max_results:
    total_results = max_results

 
  other_pages = [
    ScrapeConfig(_add_url_parameter(url, start=offset), **BASE_CONFIG)
    for offset in range(10, total_results + 10, 10)
  ]
  log.info("found total pages {} search pages", math.ceil(total_results / 10))
  async for result in SCRAPFLY.concurrent_scrape(other_pages):
    if not isinstance(result, ScrapflyScrapeError):
      data = parse_search_page(result)
      results.extend(data["results"])
    else:
      log.error(f"failed to scrape {result.api_response.config['url']}, got: {result.message}")
  return results

def parse_job_page(result: ScrapeApiResponse):
  """parse job data from job listing page"""
  data = re.findall(r"_initialData=(\{.+?\});", result.content)
  data = json.loads(data[0])
  data = data["jobInfoWrapperModel"]["jobInfoModel"]
  return {
    "description": data.get('sanitizedJobDescription', ''),
    **data["jobMetadataHeaderModel"],
    **(data["jobTagModel"] or {}),
    **data["jobInfoHeaderModel"],
  }

async def scrape_jobs(job_keys: List[str]):
  """scrape job page"""
  log.info(f"scraping {len(job_keys)} job listings")
  results = []
  urls = [
    f"https://www.indeed.com/viewjob?jk={job_key}" 
    for job_key in job_keys
  ]
  to_scrape = [ScrapeConfig(url, **BASE_CONFIG) for url in urls]
  async for result in SCRAPFLY.concurrent_scrape(to_scrape):
    results.append(parse_job_page(result))
  return results

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()

    # Modify the search URL and max_results as needed
    search_url = "https://www.indeed.com/jobs?q=your+search+query"
    max_results = 1000  # Adjust as needed

    try:
        search_results = loop.run_until_complete(scrape_search(search_url, max_results))
        job_keys = [result["jobkey"] for result in search_results]
        job_details = loop.run_until_complete(scrape_jobs(job_keys))
        print("Search results:", search_results)
        print("Job details:", job_details)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        loop.close()

## ARGPARSE for use in CLI commands     
def parse_arguments():
    parser = argparse.ArgumentParser(description="Indeed.com Job Scraper")
    parser.add_argument("--job_description", required=True, help="Job description to search for")
    parser.add_argument("--location", required=True, help="Location to search")
    return parser.parse_args()

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()

    args = parse_arguments()
    job_description = args.job_description
    location = args.location

    # Modify the search URL and max_results as needed
    search_url = f"https://www.indeed.com/jobs?q={urllib.parse.quote(job_description)}&l={urllib.parse.quote(location)}"
    max_results = 1000  # Adjust as needed

    try:
        search_results = loop.run_until_complete(scrape_search(search_url, max_results))
        job_keys = [result["jobkey"] for result in search_results]
        job_details = loop.run_until_complete(scrape_jobs(job_keys))
        print("Search results:", search_results)
        print("Job details:", job_details)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        loop.close()


def fetch_indeed_listings(job_title: str, location: str) -> List[Dict[str, any]]:
    # Construct the search URL based on job_title and location
    BASE_URL = "https://www.indeed.com/jobs?q={}&l={}"
    url = BASE_URL.format(urllib.parse.quote(job_title), urllib.parse.quote(location))
    
    # Logic to fetch and parse the first page
    result_first_page = SCRAPFLY.scrape(ScrapeConfig(url, **BASE_CONFIG))
    data_first_page = parse_search_page(result_first_page)
    results = data_first_page["results"]
    total_results = sum(category["jobCount"] for category in data_first_page["meta"])
    max_results = 30  # Limit to 30 results as per your requirement

    # Limit the total results if they exceed max_results
    if total_results > max_results:
        total_results = max_results

    # Logic to fetch and parse additional pages
    other_pages = [
        ScrapeConfig(_add_url_parameter(url, start=offset), **BASE_CONFIG)
        for offset in range(10, total_results + 10, 10)
    ]
    
    for result in SCRAPFLY.concurrent_scrape(other_pages):
        if not isinstance(result, ScrapflyScrapeError):
            data = parse_search_page(result)
            results.extend(data["results"])

    return results
