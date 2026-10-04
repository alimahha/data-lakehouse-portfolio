
from pathlib import Path

import pandas as pd
import pytest

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def athletes_silver():
    return pd.read_parquet(DATA_DIR / "athlete_events_clean.parquet")


@pytest.fixture
def fact_gold():
    return pd.read_parquet(DATA_DIR / "FactParticipation.parquet")


@pytest.fixture
def dim_athlete():
    return pd.read_parquet(DATA_DIR / "DimAthlete.parquet")


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
