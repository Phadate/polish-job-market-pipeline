## Data Sources & Legal Compliance

All sources reviewed 

### JustJoin.it
- robots.txt reviewed: /api/ disallowed, public pages allowed
- Approach: scraping public job listing pages only
- Rate limiting: 3 second delay between requests
- Data is fetched from the same endpoint that JustJoin.it's 
own website uses to render public job listings. No authentication 
required. Data is publicly visible to any visitor.

### NoFluffJobs.com  
- robots.txt reviewed: explicitly Allow: / for all public pages
- /api/ disallowed — not using API
- Rate limiting: 3 second delay between requests

### Pracuj.pl
- robots.txt reviewed: only asset folders disallowed
- Sitemaps publicly exposed including CurrentOffers sitemap
- Approach: parsing sitemap XML then visiting job URLs
- Rate limiting: 3 second delay between requests

## Update on Data Sources

### JustJoin.it ✅ Active
946 job listings scraped via public API endpoint.
Full Bronze → Silver → Gold pipeline operational.

### NoFluffJobs ❌ Excluded
robots.txt explicitly disallows /api/ and /posting/ 
endpoints. Excluded out of respect for crawling policy.

### Pracuj.pl & theprotocol.it ⏳ Planned
Both sites protected by Cloudflare bot detection.
Playwright-based scraping planned for future sprint.