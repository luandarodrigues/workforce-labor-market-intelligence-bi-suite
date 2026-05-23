# Data Model

## Modeling Approach

The semantic layer is centered on `fact_employee_monthly`, which represents one employee snapshot for the reference month. That fact is enriched by:

- `fact_attrition_risk` for modeled risk and recommendation outputs
- `fact_labor_market_monthly` for external labor market context

This keeps the BI model simple enough for direct consumption while still supporting workforce planning questions.

## Dimensions

### dim_employee

Employee profile attributes used for slicing and segmentation:

- `employee_id`
- `age_band`
- `gender`
- `education_level`
- `marital_status`
- `distance_from_home_band`

### dim_department

Organizational unit reference:

- `department_id`
- `department_name`

### dim_role

Role and market-mapping reference:

- `role_id`
- `job_role`
- `job_level`
- `role_family`
- `occupation_group`
- `role_criticality`

### dim_region

Geographic market reference:

- `region_id`
- `region_name`
- `region_type`
- `labor_market_code`

### dim_date

Monthly calendar grain:

- `date_id`
- `month`
- `quarter`
- `year`

## Facts

### fact_employee_monthly

Primary workforce table used by BI:

- `employee_id`
- `department_id`
- `role_id`
- `region_id`
- `date_id`
- `monthly_income`
- `annualized_income`
- `salary_band`
- `years_at_company`
- `years_in_current_role`
- `years_since_last_promotion`
- `overtime_flag`
- `training_times_last_year`
- `job_satisfaction`
- `environment_satisfaction`
- `work_life_balance`
- `performance_rating`
- `attrition_flag`
- `estimated_replacement_cost`

### fact_attrition_risk

Modeled risk layer:

- `employee_id`
- `date_id`
- `attrition_probability`
- `risk_band`
- `main_risk_driver`
- `recommended_action`
- `model_version`

### fact_labor_market_monthly

External market layer:

- `date_id`
- `region_id`
- `occupation_group`
- `unemployment_rate`
- `wage_index`
- `labor_demand_index`
- `external_pressure_score`

## BI-Ready Consolidated Dataset

The exported `tableau_ready_dataset.csv` and `powerbi_ready_dataset.xlsx` join facts and dimensions into a single analytical table. This consolidated layer includes:

- business keys and descriptive dimensions
- compensation, tenure, and engagement-like fields
- attrition risk outputs
- labor market context
- `retention_priority_index` as a decision-support composite field

That makes the BI layer much easier to consume without rebuilding joins or metric logic inside the dashboard tool.
