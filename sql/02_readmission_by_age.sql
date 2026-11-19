-- Healthcare Readmission Analysis
-- Query 2: 30-Day Readmission Rates by Age Group

SELECT
    age AS age_group,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM hospital_analysis
GROUP BY age
ORDER BY age;