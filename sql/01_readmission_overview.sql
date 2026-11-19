-- Healthcare Readmission Analysis
-- Query 1: Overall 30-Day Readmission Rate
-- Dataset: UCI Diabetes 130-US Hospitals

SELECT
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    COUNT(*) - SUM(readmitted_30_days) AS not_readmitted_30_days,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM hospital_analysis;