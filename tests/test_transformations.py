
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from transformations import clean_athletes, clean_wikidata


def test_athletes_duplicates_are_removed():
    raw = pd.DataFrame({
        "ID": [1, 1],
        "Age": ["20", "20"],
        "Height": ["180", "180"],
        "Weight": ["75", "75"],
        "Sport": [" swimming ", " swimming "],
        "Team": [" France ", " France "],
    })

    result = clean_athletes(raw)

    assert len(result) == 1
    assert not result.duplicated().any()


def test_athletes_numeric_columns_have_numeric_types():
    raw = pd.DataFrame({
        "ID": [1, 2],
        "Age": ["20", "unknown"],
        "Height": ["180", "175"],
        "Weight": ["75", "70"],
        "Sport": ["Swimming", "Athletics"],
        "Team": ["France", "Canada"],
    })

    result = clean_athletes(raw)

    for column in ["Age", "Height", "Weight"]:
        assert pd.api.types.is_numeric_dtype(result[column])

    assert pd.isna(result.loc[1, "Age"])


def test_athletes_text_and_missing_values_are_cleaned():
    raw = pd.DataFrame({
        "ID": [1, 2],
        "Age": ["NA", "25"],
        "Height": ["180", "175"],
        "Weight": ["75", "70"],
        "Sport": [" swimming ", "athletics"],
        "Team": [" France ", "Canada"],
    })

    result = clean_athletes(raw)

    assert pd.isna(result.loc[0, "Age"])
    assert result.loc[0, "Sport"] == "Swimming"
    assert result.loc[0, "Team"] == "France"


def test_wikidata_duplicates_and_text_are_cleaned():
    raw = pd.DataFrame({
        "athleteLabel": [" Alice ", " Alice "],
        "countryLabel": [" France ", " France "],
        "sportLabel": [" swimming ", " swimming "],
    })

    result = clean_wikidata(raw)

    assert len(result) == 1
    assert result.iloc[0]["athleteLabel"] == "Alice"
    assert result.iloc[0]["countryLabel"] == "France"
    assert result.iloc[0]["sportLabel"] == "Swimming"
