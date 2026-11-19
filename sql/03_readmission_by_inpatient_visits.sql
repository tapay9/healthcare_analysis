-- Healthcare Readmission Analysis
-- Query 3: Previous Inpatient Visits and 30-Day Readmissions

WITH inpatient_groups AS (
    SELECT
        CASE
            WHEN number_inpatient = 0 THEN '0'
            WHEN number_inpatient = 1 THEN '1'
            WHEN number_inpatient = 2 THEN '2'
            WHEN number_inpatient BETWEEN 3 AND 4 THEN '3-4'
            ELSE '5+'
        END AS inpatient_visit_group,
        readmitted_30_days
    FROM hospital_analysis
)

SELECT
    inpatient_visit_group,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM inpatient_groups
GROUP BY inpatient_visit_group
ORDER BY
    CASE inpatient_visit_group
        WHEN '0' THEN 1
        WHEN '1' THEN 2
        WHEN '2' THEN 3
        WHEN '3-4' THEN 4
        WHEN '5+' THEN 5
    END;