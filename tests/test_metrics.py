from src.exports.export_bi_files import build_attrition_rate


def test_build_attrition_rate_uses_total_attrition_over_headcount():
    assert build_attrition_rate(attrition_count=10, headcount=100) == 0.10
