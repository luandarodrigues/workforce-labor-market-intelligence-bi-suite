create or replace table executive_kpis as
select
    count(*) as headcount,
    sum(attrition_flag) * 1.0 / nullif(count(*), 0) as attrition_rate,
    avg(monthly_income) as average_monthly_base_pay,
    avg(years_at_company) as average_tenure,
    median(years_at_company) as median_tenure,
    sum(case when training_times_last_year > 0 then 1 else 0 end) * 1.0 / nullif(count(*), 0) as training_participation_rate,
    sum(case when overtime_flag = 1 then 1 else 0 end) * 1.0 / nullif(count(*), 0) as overtime_rate
from fact_employee_monthly;
