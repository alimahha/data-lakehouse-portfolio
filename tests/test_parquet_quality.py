
import pandas as pd
import pytest


@pytest.fixture
def athletes_silver(tmp_path):
    df = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Age": [25, 28, 22],
            "Height": [180.0, 175.0, 190.0],
            "Weight": [75.0, 68.0, 85.0],
            "Sport": ["Athletics", "Swimming", "Basketball"],
            "Team": ["France", "Canada", "USA"],
        }
    )

    filepath = tmp_path / "athlete_events_clean.parquet"
    df.to_parquet(filepath, index=False)
    return pd.read_parquet(filepath)


@pytest.fixture
def fact_gold(tmp_path):
    df = pd.DataFrame(
        {
            "athlete_id": [1, 2, 3],
            "Sport": ["Athletics", "Swimming", "Basketball"],
            "NOC": ["FRA", "CAN", "USA"],
            "Games": ["2016 Summer", "2020 Summer", "2012 Summer"],
            "Medal": ["Gold", None, "Bronze"],
        }
    )

    filepath = tmp_path / "FactParticipation.parquet"
    df.to_parquet(filepath, index=False)
    return pd.read_parquet(filepath)


@pytest.fixture
def dim_athlete(tmp_path):
    df = pd.DataFrame(
        {
            "athlete_id": [1, 2, 3],
            "Name": ["Athlete A", "Athlete B", "Athlete C"],
            "Sex": ["M", "F", "M"],
            "Age": [25, 28, 22],
        }
    )

    filepath = tmp_path / "DimAthlete.parquet"
    df.to_parquet(filepath, index=False)
    return pd.read_parquet(filepath)


def test_silver_file_is_not_empty(athletes_silver):
    assert not athletes_silver.empty


def test_silver_has_required_columns(athletes_silver):
    required = {"ID", "Age", "Height", "Weight", "Sport", "Team"}
    assert required.issubset(athletes_silver.columns)


def test_silver_has_no_duplicate_rows(athletes_silver):
    assert not athletes_silver.duplicated().any()


def test_silver_numeric_columns_have_numeric_types(athletes_silver):
    for column in ["Age", "Height", "Weight"]:
        assert pd.api.types.is_numeric_dtype(athletes_silver[column])


def test_gold_fact_file_is_not_empty(fact_gold):
    assert not fact_gold.empty


def test_gold_fact_has_required_columns(fact_gold):
    required = {"athlete_id", "Sport", "NOC", "Games", "Medal"}
    assert required.issubset(fact_gold.columns)


def test_dim_athlete_has_unique_ids(dim_athlete):
    assert "athlete_id" in dim_athlete.columns
    assert dim_athlete["athlete_id"].is_unique
