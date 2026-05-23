# Executive Summary

## Overview

This repository delivers a BI-ready workforce analytics product that combines internal HR data, labor market context, explainable attrition risk scoring, and reusable semantic outputs for downstream dashboards.

## Current Pipeline Output

- Headcount: `1470` employee-month records
- Attrition rate: `16.12%`
- Average monthly base pay: `6502.93`
- Average tenure: `7.01` years
- Median tenure: `5.00` years
- Training participation rate: `96.33%`
- Overtime rate: `28.30%`
- Estimated replacement cost pool: `107145624.00`

## Risk Layer

- High-risk employees: `33`
- Medium-risk employees: `538`
- Low-risk employees: `899`
- Most common modeled driver: `Mixed workforce factors`

## Source Status

- Internal HR source: `WA_Fn-UseC_-HR-Employee-Attrition.csv`
- External labor market source: `demo_bls_structure`

## Interpretation

The current build is strong enough to support executive BI questions around workforce composition, attrition concentration, risk segmentation, compensation pressure, and retention prioritization. The internal HR layer is already running on the real IBM attrition source, while the external layer remains ready for live BLS snapshots once the environment-specific fetch issue is resolved.
