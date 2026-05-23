from src.models.score_attrition_risk import risk_band_for_probability


def test_risk_band_for_probability_matches_spec_thresholds():
    assert risk_band_for_probability(0.39) == "Low Risk"
    assert risk_band_for_probability(0.40) == "Medium Risk"
    assert risk_band_for_probability(0.70) == "High Risk"
