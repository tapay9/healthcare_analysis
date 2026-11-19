-- Healthcare Readmission Analysis
-- Query 5: Medication Count and 30-Day Readmissions

WITH medication_groups AS (
    SELECT
        CASE
            WHEN num_medications BETWEEN 0 AND 5 THEN '0-5'
            WHEN num_medications BETWEEN 6 AND 10 THEN '6-10'
            WHEN num_medications BETWEEN 11 AND 15 THEN '11-15'
            WHEN num_medications BETWEEN 16 AND 20 THEN '16-20'
            ELSE '21+'
        END AS medication_group,
        readmitted_30_days
    FROM hospital_analysis
)

SELECT
    medication_group,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM medication_groups
GROUP BY medication_group
ORDER BY
    CASE medication_group
        WHEN '0-5' THEN 1
        WHEN '6-10' THEN 2
        WHEN '11-15' THEN 3
        WHEN '16-20' THEN 4
        WHEN '21+' THEN 5
    END;