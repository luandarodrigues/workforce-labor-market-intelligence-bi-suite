# Business Problem

## Core Question

How can a company combine internal employee data with external labor market context to make better decisions about retention, cost, and workforce planning?

## Business Need

Many HR and BI teams analyze attrition only after employees leave. That usually limits the conversation to reactive reporting: who exited, from which area, and in which period. This project is designed to move that discussion toward a more useful product layer by combining:

- internal workforce structure
- compensation and tenure signals
- promotion and training context
- explainable attrition risk outputs
- external labor market pressure context

## Why This Matters

In the current pipeline run, the modeled workforce includes:

- `1,470` employee-month records
- `16.12%` attrition rate
- average monthly base pay of approximately `6,502.93`
- average tenure of approximately `7.01` years
- median tenure of `5.0` years
- training participation rate of `96.33%`
- overtime rate of `28.30%`

That output is already enough to support BI-style questions such as:

- where attrition is concentrated
- which employee groups have higher modeled risk
- whether overtime and stalled progression are showing up as practical risk signals
- where labor market exposure may intensify retention pressure

## Current Risk Story

The current run also produces an attrition risk layer with:

- `33` high-risk employees
- `538` medium-risk employees
- `899` low-risk employees
- average attrition probability of approximately `0.3533`

The most common modeled drivers are:

- mixed workforce factors
- career progression risk
- overtime and work-life balance pressure

This makes the project useful not just for descriptive reporting, but for prioritization and action-oriented BI outputs.
