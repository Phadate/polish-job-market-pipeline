SELECT 
    id,
    title,
    city,
    companyName AS company_name,
    experienceLevel AS experience_level, 
    skill_name,
    skill_level
FROM {{ source('silver', 'silver_skills') }}