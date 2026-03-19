# Polish Job Market Intelligence Pipeline

![CI](https://github.com/phadate/polish-job-market-pipeline/actions/workflows/dbt_ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![dbt](https://img.shields.io/badge/dbt-1.9-orange)
![Airflow](https://img.shields.io/badge/airflow-2.9.3-green)

An automated end-to-end data pipeline that scrapes, 
transforms, and analyses the Polish tech job market daily. 
Built as a portfolio project demonstrating modern 
data engineering practices.

## Overview

This pipeline ingests daily job listings from JustJoin.it, 
the largest Polish tech job board, and transforms raw data 
into analytical insights about the Polish tech job market.

**What it reveals:**
- Most in-demand technical skills in Poland
- Salary ranges by city, experience level, and contract type
- Remote vs hybrid vs office work distribution
- Market trends across 900+ daily job listings

## Architecture
```
JustJoin.it API
      │
      ▼
┌─────────────────┐
│   Bronze Layer  │  Raw JSON files
│ Azure Blob      │  partitioned by date
│ Storage         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Silver Layer  │  Cleaned Delta tables
│ Azure           │  silver_jobs
│ Databricks      │  silver_skills
│ (PySpark)       │  silver_salaries
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gold Layer    │  Analytical mart models
│ dbt Cloud       │  mart_top_skills
│ (SQL models)    │  mart_salary_by_city
│                 │  mart_salary_by_level
│                 │  mart_workplace_trends
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Orchestration  │  Apache Airflow on Docker
│  CI/CD          │  GitHub Actions
└─────────────────┘
```

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Ingestion | Python + Requests | JustJoin.it API scraper |
| Storage | Azure Blob Storage | Bronze layer raw JSON |
| Transformation | Azure Databricks + PySpark | Silver Delta tables |
| Modelling | dbt Cloud | Gold layer mart models |
| Orchestration | Apache Airflow + Docker | Daily pipeline scheduling |
| CI/CD | GitHub Actions | Automated dbt testing on push |
| Version Control | Git + GitHub | Source code management |

## Data Sources

### JustJoin.it ✅ Active
Poland's largest tech job board. 900+ listings scraped 
daily via public API endpoint. Full Bronze → Silver → 
Gold pipeline operational.

### NoFluffJobs ❌ Excluded
robots.txt explicitly disallows /api/ and /posting/ 
endpoints. Excluded out of respect for crawling policy.

### Pracuj.pl & theprotocol.it ⏳ Planned
Both sites protected by Cloudflare bot detection. 
Playwright-based scraping planned for future sprint.

## Key Market Insights (February 2026)

Derived from 946 job listings scraped from JustJoin.it.

### Most In-Demand Skills
| Rank | Skill | Job Mentions |
|------|-------|-------------|
| 1 | Python | 221 |
| 2 | SQL | 164 |
| 3 | Java | 140 |
| 4 | AWS | 122 |
| 5 | Docker | 107 |
| 6 | Kubernetes | 107 |
| 7 | TypeScript | 91 |
| 8 | Azure | 87 |

### Work Model Distribution
| Type | Jobs | Percentage |
|------|------|-----------|
| Hybrid | 440 | 47.8% |
| Remote | 426 | 46.3% |
| Office | 54 | 5.9% |

### Salary by Experience (PLN/month, B2B)
| Level | Min | Max |
|-------|-----|-----|
| Junior | 4,300 | 6,500 |
| Mid | 15,600 | 21,000 |
| Senior | 22,400 | 29,000 |

> **Note:** Salary figures require normalisation of 
> salary units (hourly/daily/monthly) for accurate 
> comparison. Planned improvement in next sprint.


## Project Structure
```
polish-job-market-pipeline/
├── airflow/                    # Orchestration
│   ├── dags/
│   │   └── main_pipeline.py   # Main DAG definition
│   ├── pipelines/
│   │   ├── justjoin.py        # Scraper
│   │   └── upload_to_blob.py  # Azure upload
│   ├── docker-compose.yml
│   └── requirements.txt
├── databricks/
│   └── silver_transformation.ipynb  # PySpark notebook
├── dbt_project/                # dbt models
│   └── models/
│       ├── staging/
│       │   ├── stg_jobs.sql
│       │   ├── stg_skills.sql
│       │   ├── stg_salaries.sql
│       │   └── _properties.yml
│       └── marts/
│           ├── mart_top_skills.sql
│           ├── mart_salary_by_city.sql
│           ├── mart_salary_by_level.sql
│           └── mart_workplace_trends.sql
├── .github/
│   └── workflows/
│       └── dbt_ci.yml         # CI/CD pipeline
└── README.md
```

## How to Run

### Prerequisites
- Docker Desktop
- Azure account with Blob Storage
- Databricks workspace
- dbt Cloud account

### Setup

1. Clone the repository
```bash
git clone https://github.com/phadate/polish-job-market-pipeline
cd polish-job-market-pipeline
```

2. Configure environment variables
```bash
cp airflow/.env.example airflow/.env
# Fill in your credentials
```

3. Start Airflow
```bash
cd airflow
docker-compose up -d
```

4. Open Airflow UI
```
http://localhost:8080
admin / admin
```

5. Trigger the pipeline
```
DAGs → polish_job_market_pipeline → Trigger
```
## Known Limitations and Backlog

### Data Quality
- [ ] Normalise salary units to monthly PLN 
      (hourly × 168, daily × 21, yearly ÷ 12)
- [ ] Standardise city names 
      (Warsaw/warsaw/Warszawa → Warszawa)
- [ ] Fix camelCase columns in Silver layer
      (companyName → company_name)

### Pipeline
- [ ] Add theprotocol.it scraper using Playwright
- [ ] Add Pracuj.pl scraper
- [ ] Deploy Airflow to cloud 
      (Azure Container Instance or Astronomer)
- [ ] Add email alerting on pipeline failure

### Analysis
- [ ] Salary trends over time
- [ ] Skills demand trends month over month
- [ ] Company hiring frequency analysis
