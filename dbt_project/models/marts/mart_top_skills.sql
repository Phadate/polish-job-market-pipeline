-- What are the most in-demand skills in Poland right now?
SELECT 
    skill_name,
    COUNT(skill_name) AS job_count
FROM {{ref('stg_skills')}}
GROUP BY skill_name
HAVING COUNT(skill_name) > 5
ORDER BY job_count DESC