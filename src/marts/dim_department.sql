create or replace table dim_department as
select
    row_number() over (order by department) as department_id,
    department as department_name
from (select distinct department from stage_hr);
