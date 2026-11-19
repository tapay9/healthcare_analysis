-- Healthcare Readmission Analysis
-- Query 4: Length of Hospital Stay and 30-Day Readmissions

SELECT
    time_in_hospital AS hospital_stay_days,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM hospital_analysis
GROUP BY time_in_hospital
ORDER BY time_in_hospital;