-- What are the most in-demand skills in Poland right now?
SELECT 
  workplace_type,
  COUNT(*) AS job_count,
  COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM {{ref('stg_jobs')}} 
GROUP BY workplace_type
ORDER BY job_count DESC