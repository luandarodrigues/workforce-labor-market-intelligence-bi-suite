create or replace table dim_region as
select distinct
    region_id,
    'United States' as region_name,
    'country' as region_type,
    'US' as labor_market_code
from stage_hr;
