import duckdb

print("========== ANALYTICS QUERIES ==========\n")

# Connect to the DuckDB database
con = duckdb.connect("../data/olympics.duckdb")

# ==================================================
# Query 1: Top 10 countries by total medal count
# ==================================================

print("QUERY 1: Top 10 countries by total medals")

result = con.execute("""
    SELECT
        NOC,
        COUNT(*) AS total_medals
    FROM FactParticipation
    WHERE Medal <> 'NA'
    GROUP BY NOC
    ORDER BY total_medals DESC
    LIMIT 10
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# ==================================================
# Query 2: Sports with the highest number of gold medals
# ==================================================

print("QUERY 2: Sports with the most gold medals")

result = con.execute("""
    SELECT
        Sport,
        COUNT(*) AS gold_medals
    FROM FactParticipation
    WHERE Medal = 'Gold'
    GROUP BY Sport
    ORDER BY gold_medals DESC
    LIMIT 10
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# ==================================================
# Query 3: Average age of medal-winning athletes
# ==================================================

print("QUERY 3: Average age of medal winners")

result = con.execute("""
    SELECT
        AVG(Age) AS average_age
    FROM DimAthlete
    WHERE athlete_id IN (
        SELECT athlete_id
        FROM FactParticipation
        WHERE Medal <> 'NA'
    )
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# ==================================================
# Query 4: Number of athletes by gender
# ==================================================

print("QUERY 4: Number of athletes by gender")

result = con.execute("""
    SELECT
        Sex,
        COUNT(*) AS athlete_count
    FROM DimAthlete
    WHERE Sex IS NOT NULL
    GROUP BY Sex
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# ==================================================
# Query 5: Participation count by Olympic Games edition
# ==================================================

print("QUERY 5: Participation count by Olympic Games")

result = con.execute("""
    SELECT
        Games,
        COUNT(*) AS participations
    FROM FactParticipation
    WHERE Games IS NOT NULL
    GROUP BY Games
    ORDER BY participations DESC
    LIMIT 10
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# ==================================================
# Query 6: Number of medals awarded by season
# ==================================================

print("QUERY 6: Medals awarded by Olympic season")

result = con.execute("""
    SELECT
        o.Season,
        COUNT(*) AS medal_count
    FROM FactParticipation f
    JOIN DimOlympics o
        ON f.Games = o.Games
    WHERE f.Medal <> 'NA'
    GROUP BY o.Season
""").fetchdf()

print(result)
print("\n" + "=" * 60 + "\n")


# Close the database connection
con.close()

print("========== ANALYTICS COMPLETED ==========")