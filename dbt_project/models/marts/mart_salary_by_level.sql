-- What is the salary gap between junior, mid, and senior roles?
SELECT 
    j.experience_level,
    s.contract_type,
    AVG(s.salary_min) AS avg_salary_min,
    AVG(s.salary_max) AS avg_salary_max,
    COUNT(DISTINCT s.id) AS job_count
FROM {{ ref('stg_salaries') }} s
JOIN {{ ref('stg_jobs') }} j 
ON s.id = j.id
WHERE salary_disclosed = true
GROUP BY j.experience_level, s.contract_type
ORDER BY avg_salary_max DESC