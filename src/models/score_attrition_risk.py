from __future__ import annotations


def risk_band_for_probability(probability: float) -> str:
    if probability >= 0.70:
        return "High Risk"
    if probability >= 0.40:
        return "Medium Risk"
    return "Low Risk"


def recommendation_for_row(row: dict) -> str:
    if row["overtime_flag"] == 1 and row["work_life_balance"] <= 2:
        return "Review workload and manager allocation"
    if row["years_since_last_promotion"] >= 3 and row["performance_rating"] >= 3:
        return "Prioritize career progression review"
    return "Monitor and discuss retention plan"
