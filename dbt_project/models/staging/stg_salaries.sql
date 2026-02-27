SELECT
    id,
    title,
    city,
    companyName as company_name,
    experienceLevel as experience_level,
    contract_type,
    salary_min,
    salary_max,
    currency,
    salary_unit,
    is_gross,
    salary_disclosed
FROM {{ source('silver', 'silver_salaries') }}
WHERE salary_disclosed = true
