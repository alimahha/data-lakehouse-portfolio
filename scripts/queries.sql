-- ============================================
-- QUERY 1 : Top 10 countries by total medals
-- ============================================

SELECT
    NOC,
    COUNT(*) AS total_medals
FROM FactParticipation
WHERE Medal <> 'NA'
GROUP BY NOC
ORDER BY total_medals DESC
LIMIT 10;


-- ============================================
-- QUERY 2 : Sports with the most gold medals
-- ============================================

SELECT
    Sport,
    COUNT(*) AS gold_medals
FROM FactParticipation
WHERE Medal = 'Gold'
GROUP BY Sport
ORDER BY gold_medals DESC
LIMIT 10;


-- ============================================
-- QUERY 3 : Average age of medal-winning athletes
-- ============================================

SELECT
    AVG(Age) AS average_age
FROM DimAthlete
WHERE athlete_id IN (
    SELECT athlete_id
    FROM FactParticipation
    WHERE Medal <> 'NA'
);


-- ============================================
-- QUERY 4 : Number of athletes by gender
-- ============================================

SELECT
    Sex,
    COUNT(*) AS athlete_count
FROM DimAthlete
WHERE Sex IS NOT NULL
GROUP BY Sex;


-- ============================================
-- QUERY 5 : Participation count by Olympic Games
-- ============================================

SELECT
    Games,
    COUNT(*) AS participations
FROM FactParticipation
WHERE Games IS NOT NULL
GROUP BY Games
ORDER BY participations DESC
LIMIT 10;


-- ============================================
-- QUERY 6 : Medals awarded by Olympic season
-- ============================================

SELECT
    o.Season,
    COUNT(*) AS medal_count
FROM FactParticipation f
JOIN DimOlympics o
    ON f.Games = o.Games
WHERE f.Medal <> 'NA'
GROUP BY o.Season;