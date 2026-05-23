create or replace table dim_role as
select
    row_number() over (order by s.job_role) as role_id,
    s.job_role,
    1 as job_level,
    m.role_family,
    m.occupation_group,
    m.role_criticality
from (select distinct job_role from stage_hr) s
left join role_market_mapping m on s.job_role = m.job_role;
