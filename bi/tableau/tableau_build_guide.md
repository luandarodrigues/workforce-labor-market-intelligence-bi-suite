# Tableau Build Guide

## Source File

Use `data/bi_exports/tableau_ready_dataset.csv` as the single Tableau source.

## Build Order

1. Connect the CSV in Tableau.
2. Review field types and convert `date_id` if needed for display.
3. Create the calculated fields listed in `calculated_fields.md`.
4. Build the individual sheets from `sheet_mapping.csv`.
5. Assemble the three dashboards from `dashboard_blueprint.md`.
6. Apply final titles, subtitles, tooltips, and annotations from `public_dashboard_copy.md`.

## Expected Dashboards

- Executive Overview
- Attrition Risk
- Labor Market Context

## Notes

- Keep business logic in the exported dataset whenever possible.
- Avoid rebuilding semantic metrics inside Tableau unless the calculation is purely presentational.
- Use dashboard actions sparingly so the public portfolio version stays easy to navigate.
