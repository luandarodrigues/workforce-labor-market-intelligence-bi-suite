create or replace table fact_attrition_risk as
select
    employee_id,
    date_id,
    least(
        0.95,
        round(
            0.15
            + overtime_flag * 0.20
            + case when work_life_balance <= 2 then 0.20 else 0 end
            + case when years_since_last_promotion >= 3 then 0.15 else 0 end
            + case when monthly_income < 5000 then 0.10 else 0 end,
            2
        )
    ) as attrition_probability,
    case
        when least(
            0.95,
            round(
                0.15
                + overtime_flag * 0.20
                + case when work_life_balance <= 2 then 0.20 else 0 end
                + case when years_since_last_promotion >= 3 then 0.15 else 0 end
                + case when monthly_income < 5000 then 0.10 else 0 end,
                2
            )
        ) >= 0.70 then 'High Risk'
        when least(
            0.95,
            round(
                0.15
                + overtime_flag * 0.20
                + case when work_life_balance <= 2 then 0.20 else 0 end
                + case when years_since_last_promotion >= 3 then 0.15 else 0 end
                + case when monthly_income < 5000 then 0.10 else 0 end,
                2
            )
        ) >= 0.40 then 'Medium Risk'
        else 'Low Risk'
    end as risk_band,
    case
        when overtime_flag = 1 and work_life_balance <= 2 then 'Overtime and work-life balance'
        when years_since_last_promotion >= 3 and performance_rating >= 3 then 'Career progression'
        else 'Mixed workforce factors'
    end as main_risk_driver,
    case
        when overtime_flag = 1 and work_life_balance <= 2 then 'Review workload and manager allocation'
        when years_since_last_promotion >= 3 and performance_rating >= 3 then 'Prioritize career progression review'
        else 'Monitor and discuss retention plan'
    end as recommended_action,
    'baseline_v1' as model_version
from fact_employee_monthly;
