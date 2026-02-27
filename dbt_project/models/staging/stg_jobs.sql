select
    id,
    slug,
    title,
    city,
    street,
    companyName as company_name,
    companySize as company_size,
    countryCode as country_code,
    experienceLevel as experience_level,
    workplaceType as workplace_type,
    workingTime as working_time,
    publishedAt as published_at,
    isActive as is_active,
    category
from {{ source('silver', 'silver_jobs') }}
where isActive = true