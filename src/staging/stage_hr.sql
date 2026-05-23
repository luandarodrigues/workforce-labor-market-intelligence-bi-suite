create or replace table stage_hr as
select
    employee_number as employee_id,
    age,
    department,
    job_role,
    monthly_income,
    monthly_income * 12 as annualized_income,
    years_at_company,
    years_in_current_role,
    years_since_last_promotion,
    overtime_flag,
    training_times_last_year,
    job_satisfaction,
    environment_satisfaction,
    work_life_balance,
    performance_rating,
    attrition_flag,
    gender,
    education as education_level,
    marital_status,
    distance_from_home,
    region_id
from hr_raw;
