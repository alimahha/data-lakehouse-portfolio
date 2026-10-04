import pandas as pd


def clean_athletes(athletes: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données des athlètes avant leur stockage en Silver."""
    athletes = athletes.copy()

    athletes.replace(["NA", "NULL"], pd.NA, inplace=True)

    for column in ["Age", "Height", "Weight"]:
        athletes[column] = pd.to_numeric(
            athletes[column], errors="coerce"
        )

    athletes["Sport"] = athletes["Sport"].str.strip().str.title()
    athletes["Team"] = athletes["Team"].str.strip()

    athletes.drop_duplicates(inplace=True)
    return athletes


def clean_wikidata(wiki: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données Wikidata avant leur stockage en Silver."""
    wiki = wiki.copy()

    wiki.replace(["NA", "NULL"], pd.NA, inplace=True)
    wiki.drop_duplicates(inplace=True)

    wiki["athleteLabel"] = wiki["athleteLabel"].str.strip()
    wiki["countryLabel"] = wiki["countryLabel"].str.strip()
    wiki["sportLabel"] = wiki["sportLabel"].str.strip().str.title()

    return wiki
