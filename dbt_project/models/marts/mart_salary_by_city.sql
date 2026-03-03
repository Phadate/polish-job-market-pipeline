-- What is the average salary by city for each contract type?
SELECT 
  city,
  contract_type,
  AVG(salary_min) AS avg_salary_min,
  AVG(salary_max) AS avg_salary_max
FROM {{ref('stg_salaries')}}
WHERE salary_disclosed = true 
GROUP BY city, contract_type
ORDER BY avg_salary_max DESC