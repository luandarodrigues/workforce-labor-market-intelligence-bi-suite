from pathlib import Path

import duckdb


def test_stage_hr_sql_creates_expected_derived_fields(tmp_path: Path):
    con = duckdb.connect(str(tmp_path / "test.duckdb"))
    con.execute(
        """
        create table hr_raw(
            employee_number int,
            age int,
            department varchar,
            job_role varchar,
            monthly_income int,
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
            education int,
            marital_status varchar,
            distance_from_home int,
            region_id varchar
        )
        """
    )
    con.execute(
        """
        insert into hr_raw values
        (1, 34, 'Sales', 'Sales Executive', 5000, 5, 2, 1, 1, 3, 3, 3, 2, 3, 1, 'Female', 3, 'Single', 8, 'us_national')
        """
    )
    sql = Path("src/staging/stage_hr.sql").read_text(encoding="utf-8")
    con.execute(sql)
    row = con.execute("select annualized_income from stage_hr").fetchone()
    assert row[0] == 60000
