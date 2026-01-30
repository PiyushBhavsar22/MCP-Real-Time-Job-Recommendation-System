from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Fetch LinkedIn jobs based on search query and location
def fetch_linkedin_jobs(search_query, location = "ireland", rows=100):
    run_input = {
        "title": search_query,
        "loaction": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroup": ["RESIDENTIAL"],
        }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

# Fetch Indeed jobs based on search query and location
def fetch_indeed_jobs(search_query, location = "ireland", rows=100):
    run_input = {
        "keywords": search_query,
        "maxJobs": 60,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs