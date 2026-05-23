create or replace table dim_employee as
select
    employee_id,
    case
        when age <= 29 then '18-29'
        when age between 30 and 39 then '30-39'
        when age between 40 and 49 then '40-49'
        else '50+'
    end as age_band,
    gender,
    education_level,
    marital_status,
    case
        when distance_from_home <= 5 then '0-5'
        when distance_from_home <= 10 then '6-10'
        else '11+'
    end as distance_from_home_band
from stage_hr;
