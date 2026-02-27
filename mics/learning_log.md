## 2026-02-24
- Learned PySpark select(), withColumn(), filter(), explode()
- 946 jobs loaded from Azure Blob into Databricks
- Silver layer skills and salaries tables structured
- Stopped at explode concept

## 2026-02-26
- what is dbt
"dbt transforms raw warehouse data into trusted data products. You write simple SQL select statements, and dbt handles the heavy lifting by creating modular, maintainable data models that power analytics, operations, and AI, replacing the need for complex and fragile transformation code."

#### What I Built
- Configured dbt Core locally and dbt Cloud for the project
- Connected dbt Cloud to Azure Databricks Unity Catalog
- Registered Silver Delta tables as managed tables 
  in Unity Catalog (job_pipeline_databricks.silver)
- Built three staging models:
  - stg_jobs — active job listings with clean snake_case columns
  - stg_skills — one row per skill per job
  - stg_salaries — disclosed salaries in original currency only

#### What I Learned
- dbt models are just SELECT statements — 
  dbt handles CREATE/DROP automatically
- source() references external tables defined in sources.yml
- ref() references other dbt models and manages dependencies
- Staging models rename and clean, mart models aggregate and analyse
- Unity Catalog is stricter than Hive Metastore — 
  tables must be registered properly before dbt can access them
- profiles.yml must never live inside a git repo — 
  credentials belong in dbt Cloud UI or ~/.dbt/ only
- .gitkeep forces Git to track empty folders
- dbt Cloud lineage graph shows visual model dependencies

#### Challenges Solved
- dbt Cloud subdirectory configuration for monorepo structure
- Unity Catalog WASBS path restriction — 
  solved by registering managed Delta tables
- profiles.yml accidentally created in repo — 
  caught before committing, token regenerated

  