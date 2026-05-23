# Tableau Calculated Fields

## High Risk Flag

```tableau
IF [risk_band] = "High Risk" THEN 1 ELSE 0 END
```

## High Risk Employees

```tableau
SUM([High Risk Flag])
```

## Average Risk Score

```tableau
AVG([attrition_probability])
```

## External Pressure Label

```tableau
IF [external_pressure_score] >= 0.66 THEN "High"
ELSEIF [external_pressure_score] >= 0.33 THEN "Medium"
ELSE "Low"
END
```

## Retention Priority Tier

```tableau
IF [retention_priority_index] >= 0.70 THEN "Critical"
ELSEIF [retention_priority_index] >= 0.50 THEN "Elevated"
ELSE "Monitor"
END
```

## Attrition Rate Percent

```tableau
AVG([attrition_flag])
```

Format this field as a percentage in Tableau instead of multiplying it inside the formula.
