# Model Card

## Model Purpose

The attrition model is used as a decision-support layer inside a broader workforce analytics product. It is not the sole deliverable of the repository. Its role is to estimate employee attrition risk, classify employees into interpretable risk bands, and support BI segmentation with an explainable output.

## Target

- `attrition_flag`

## Current Modeling Approach

The repository is structured to support explainable baseline models such as `Logistic Regression` and challenger approaches such as `Random Forest`. The current implementation uses governed scoring logic aligned with the project spec so that the pipeline remains executable, explainable, and easy to defend in interview settings.

Risk bands:

- `Low Risk`: 0.00 to 0.39
- `Medium Risk`: 0.40 to 0.69
- `High Risk`: 0.70 to 1.00

## Main Feature Themes

The current scoring logic is centered on factors that are defensible in a workforce context:

- overtime
- work-life balance
- years since last promotion
- monthly income
- performance rating

## Recommendation Layer

The score is paired with a recommendation layer so the output feels like a BI product rather than a raw probability table:

- workload review for overtime and work-life imbalance
- career progression review for stalled progression with solid performance
- monitoring plan for mixed-factor cases

## Appropriate Use

This model is appropriate for:

- portfolio demonstration
- BI prototyping
- workforce analytics storytelling
- explainable risk segmentation

It is not appropriate for:

- automated employment decisions
- production-grade HR intervention without validation
- causal claims about attrition behavior

## Limitations

- The internal HR source is the IBM HR attrition dataset, which is a fictional educational dataset rather than a production HRIS extract
- The current implementation uses a simplified workforce-month snapshot design
- The external labor market enrichment layer is schema-ready but not yet fully live from BLS in this environment
- The current score should be treated as a governed baseline output, not as a production-calibrated risk model
