# Metric Definitions

## Standard Workforce Metrics

These measures stay close to common workforce analytics usage.

### Headcount

- Count of employee records in the reference workforce month

### Attrition Rate

- Employees with `attrition_flag = 1` divided by total employees in the reference population

### Average Monthly Base Pay

- Mean `monthly_income` in the reference workforce month

### Average Tenure

- Mean `years_at_company`

### Median Tenure

- Median `years_at_company`

### Training Participation Rate

- Employees with `training_times_last_year > 0` divided by total employees

### Overtime Rate

- Employees with `overtime_flag = 1` divided by total employees

## Product-Specific Decision-Support Metrics

These measures are governed product outputs rather than universal HR standards.

### Attrition Probability

- Employee-level risk score derived from workload, work-life balance, promotion delay, pay, and performance-related conditions

### Risk Band

- Categorical classification of attrition probability into `Low Risk`, `Medium Risk`, or `High Risk`

### Main Risk Driver

- Primary explanation label assigned by the current scoring logic

### Recommended Action

- Suggested retention-oriented response derived from the employee risk profile

### Estimated Replacement Cost

- `annualized_income` multiplied by a role-criticality-based multiplier in the semantic layer

### External Pressure Score

- Normalized labor market pressure value intended to summarize external market tension for an occupation group

### Attrition Risk Rate Flag

- Binary indicator used in BI outputs to identify employees in the `High Risk` band

### Retention Priority Index

- Composite decision-support score combining attrition probability, external pressure, and role criticality

## Conditional Or Future-State Metrics

These are valid workforce metrics but should remain secondary until stronger source data is introduced.

### Voluntary Attrition Rate

- The current internal source does not provide a robust termination reason split

### Promotion Rate

- The current internal source does not provide a true monthly promotion event history
