
import pandas as pd


def test_silver_athletes_has_required_columns():
    athletes = pd.DataFrame({
        "ID": [1, 2],
        "Age": [20, 25],
        "Sport": ["Swimming", "Athletics"],
        "Team": ["France", "Canada"],
    })

    required_columns = {"ID", "Age", "Sport", "Team"}

    assert required_columns.issubset(athletes.columns)


def test_silver_athlete_ids_are_not_missing():
    athletes = pd.DataFrame({
        "ID": [1, 2, 3],
        "Sport": ["Swimming", "Athletics", "Cycling"],
    })

    assert athletes["ID"].notna().all()


def test_silver_athlete_ids_are_unique():
    athletes = pd.DataFrame({
        "ID": [1, 2, 3],
        "Sport": ["Swimming", "Athletics", "Cycling"],
    })

    assert athletes["ID"].is_unique


def test_gold_fact_has_required_columns():
    fact = pd.DataFrame({
        "athlete_id": [1, 2],
        "Sport": ["Swimming", "Athletics"],
        "NOC": ["FRA", "CAN"],
        "Games": ["2000 Summer", "2004 Summer"],
        "Medal": ["Gold", None],
    })

    required_columns = {"athlete_id", "Sport", "NOC", "Games", "Medal"}

    assert required_columns.issubset(fact.columns)


def test_gold_fact_athlete_ids_are_not_missing():
    fact = pd.DataFrame({
        "athlete_id": [1, 2, 3],
        "Sport": ["Swimming", "Athletics", "Cycling"],
    })

    assert fact["athlete_id"].notna().all()
