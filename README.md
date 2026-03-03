## Data Sources & Legal Compliance

All sources reviewed on [today's date].

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

---
**Note:** Salary figures require normalisation of 
salary units (hourly/daily/monthly) for accurate 
comparison. This is a planned Silver layer improvement.


## Key Market Insights (February 2026)

### Work Model Distribution (946 listings)
- Hybrid dominates at 47.8% of all listings
- Remote nearly equal at 46.3%  
- Full office work represents only 5.9% of tech jobs
- Polish tech market has effectively eliminated 
  mandatory office work

### Most In-Demand Skills
- Python #1 (221 mentions)
- SQL #2 (164 mentions)
- AWS outpaces Azure (122 vs 87)
- Docker and Kubernetes tied at 107

### Salary by Experience Level (PLN/month)
- Junior B2B:    4 300 - 6 500
- Mid B2B:      15 600 - 21 000
- Senior B2B:   22 400 - 29 000