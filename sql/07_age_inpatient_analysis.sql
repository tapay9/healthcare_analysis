-- Query 7: Age Group and Previous Inpatient Visits

WITH age_inpatient_groups AS (
    SELECT
        age AS age_group,

        CASE
            WHEN number_inpatient = 0 THEN '0 visits'
            WHEN number_inpatient BETWEEN 1 AND 2 THEN '1-2 visits'
            ELSE '3+ visits'
        END AS inpatient_history,

        readmitted_30_days
    FROM hospital_analysis
)

SELECT
    age_group,
    inpatient_history,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM age_inpatient_groups
GROUP BY age_group, inpatient_history
ORDER BY
    age_group,
    CASE inpatient_history
        WHEN '0 visits' THEN 1
        WHEN '1-2 visits' THEN 2
        ELSE 3
    END;