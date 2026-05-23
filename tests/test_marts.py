from pathlib import Path

import duckdb


def test_fact_employee_monthly_has_one_row_per_employee_month(tmp_path: Path):
    con = duckdb.connect(str(tmp_path / "test.duckdb"))
    con.execute(
        """
        create table stage_hr(
            employee_id int,
            age int,
            department varchar,
            job_role varchar,
            monthly_income int,
            annualized_income int,
            years_at_company int,
            years_in_current_role int,
            years_since_last_promotion int,
            overtime_flag int,
            training_times_last_year int,
            job_satisfaction int,
            environment_satisfaction int,
            work_life_balance int,
            performance_rating int,
            attrition_flag int,
            gender varchar,
            education_level int,
            marital_status varchar,
            distance_from_home int,
            region_id varchar
        )
        """
    )
    con.execute(
        """
        insert into stage_hr values
        (1, 34, 'Sales', 'Sales Executive', 5000, 60000, 5, 2, 1, 1, 3, 3, 3, 2, 3, 1, 'Female', 3, 'Single', 8, 'us_national')
        """
    )
    con.execute("create table role_market_mapping(job_role varchar, occupation_group varchar, role_family varchar, role_criticality varchar)")
    con.execute("insert into role_market_mapping values ('Sales Executive', 'Sales Occupations', 'Sales', 'high')")
    con.execute(Path("src/marts/dim_department.sql").read_text(encoding="utf-8"))
    con.execute(Path("src/marts/dim_role.sql").read_text(encoding="utf-8"))
    fact_sql = Path("src/marts/fact_employee_monthly.sql").read_text(encoding="utf-8")
    con.execute(Path("src/marts/dim_date.sql").read_text(encoding="utf-8"))
    con.execute(fact_sql)
    assert con.execute("select count(*) from fact_employee_monthly").fetchone()[0] == 1
