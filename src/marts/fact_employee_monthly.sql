create or replace table fact_employee_monthly as
select
    s.employee_id,
    d.department_id,
    r.role_id,
    s.region_id,
    dd.date_id,
    s.monthly_income,
    case
        when s.monthly_income < 4500 then 'Low'
        when s.monthly_income < 6500 then 'Mid'
        else 'High'
    end as salary_band,
    s.years_at_company,
    s.years_in_current_role,
    s.years_since_last_promotion,
    s.overtime_flag,
    s.training_times_last_year,
    s.job_satisfaction,
    s.environment_satisfaction,
    s.work_life_balance,
    s.performance_rating,
    s.attrition_flag,
    s.annualized_income,
    s.annualized_income * case when coalesce(r.role_criticality, 'medium') = 'high' then 1.2 else 0.8 end as estimated_replacement_cost
from stage_hr s
join dim_department d on s.department = d.department_name
join dim_role r on s.job_role = r.job_role
cross join dim_date dd;
