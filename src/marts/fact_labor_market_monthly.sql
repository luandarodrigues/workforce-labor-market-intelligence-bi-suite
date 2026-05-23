create or replace table fact_labor_market_monthly as
select
    date_id,
    region_id,
    occupation_group,
    unemployment_rate,
    wage_index,
    labor_demand_index,
    external_pressure_score
from stage_labor_market;
