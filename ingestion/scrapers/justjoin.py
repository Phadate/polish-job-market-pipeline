import requests
from bs4 import BeautifulSoup
from lxml import etree

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



all_job_offer_urls = get_sitemap_urls(sitemap_url=initial_sitemap_index_url, headers=header)

print(f"\nTotal job offer URLs found: {len(all_job_offer_urls)}")
for url in all_job_offer_urls[:10]:  # Print first 10 for example
    print(url)


def get_salaries():
    pass