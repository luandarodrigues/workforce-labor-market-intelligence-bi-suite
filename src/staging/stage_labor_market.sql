create or replace table stage_labor_market as
select
    date_id,
    region_id,
    occupation_group,
    series_id,
    year,
    period,
    unemployment_rate,
    wage_index,
    labor_demand_index,
    external_pressure_score
from labor_market_raw;
