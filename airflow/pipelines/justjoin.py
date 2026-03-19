import json
import os
from datetime import datetime
from time import sleep
import requests
from lxml import etree


today = datetime.now().strftime("%Y-%m-%d")
# Checkpoint Logic
BASE_DIR = os.environ.get('AIRFLOW_HOME',
           os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BRONZE_BASE = os.path.join(BASE_DIR, 'data', 'bronze', 'justjoin', today)
CHECKPOINT_FILE = os.path.join(BRONZE_BASE, 'scraped.txt')

if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        scraped_slugs = set(f.read().splitlines())
else:
    scraped_slugs = set()

initial_sitemap_index_url = "https://justjoin.it/sitemaps/active-jobs.xml"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

def get_sitemap_urls(sitemap_url, headers):
    urls = []
    try:
        response = requests.get(sitemap_url, headers=headers)

        response.raise_for_status()  # Raise an exception for HTTP errors

        root = etree.fromstring(response.content)

        # Check if it's a sitemap index or a regular sitemap
        #  index has <sitemapindex> root, individual sitemap has <urlset> root
        if root.tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex':
            for sitemap_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                print(f"Found sitemap index entry: {loc}")
                # Recursively get URLs from sub-sitemaps
                urls.extend(get_sitemap_urls(loc, header))
        elif root.tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset':
            for url_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                urls.append(loc)
        else:
            print(f"Unknown sitemap type for {sitemap_url}. Root tag: {root.tag}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {sitemap_url}: {e}")
    except etree.ParseError as e:
        print(f"Error parsing XML from {sitemap_url}: {e}")

    return urls



def get_api_urls(jobs_urls):
    """
    function takes in all the urls extracted from the xml, format it for the api route
    """
    base = "https://justjoin.it/api/candidate-api/offers/"

    api_urls = {}
    if jobs_urls is not None:
        for url in jobs_urls[:1000]:
            slug = url.split("/")[-1]
            api_url = base + slug
            api_urls[slug] = api_url
    else:
        return None

    return api_urls


def write_json_to_file(slug, website_data):
    """
    receive the slug and save the file
    """
    os.makedirs(BRONZE_BASE, exist_ok=True)

    with open(os.path.join(BRONZE_BASE, f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump(website_data, f, ensure_ascii=False, indent=4)
        print(f"{slug} successfully saved!")

    with open(CHECKPOINT_FILE, "a") as w:
        w.write(slug + "\n")

def get_job_details(job_api_urls: dict, headers: dict):
    """
    receive the jobs urls, make a request, and save the data
    """
    for slug, url in job_api_urls.items():

        if slug in scraped_slugs:
            print(f"Already scraped, skipping: {slug}")
            continue
        sleep(2)
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            json_data = r.json()
        except requests.exceptions.HTTPError as e:
            print( f"HTTP_Error {e}")
        except requests.exceptions.Timeout as e:
            print(f"we ran out of time {e}")
        else:
            write_json_to_file(slug, json_data)

def main():
    
    today = datetime.now().strftime("%Y-%m-%d")
    # Checkpoint Logic
    CHECKPOINT_FILE = f"../../data/bronze/justjoin/{today}/scraped.txt"

    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            scraped_slugs = set(f.read().splitlines())
    else:
        scraped_slugs = set()

    initial_sitemap_index_url = "https://justjoin.it/sitemaps/active-jobs.xml"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    all_job_offer_urls = get_sitemap_urls(sitemap_url=initial_sitemap_index_url, headers=header)
    print(f"\nTotal job offer URLs found: {len(all_job_offer_urls)}")

    job_urls_api = get_api_urls(all_job_offer_urls)

    get_job_details(job_urls_api, headers=header)

if __name__ == "__main__":
    main()